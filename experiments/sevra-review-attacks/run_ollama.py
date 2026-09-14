#!/usr/bin/env python3
"""The SEVRA cases on local Ollama models: both arms, scored by cases/oracle.py.

The prompts are the ones the hosted runs in results/grid.jsonl used
(arms/build.py, sent as one user message with no system prompt), and the
verdict is the same fixed oracle. Nothing the model writes is run: the
committed file is read by one text rule per case. Talks only to a local Ollama
at http://localhost:11434. Standard library only.

Needs cases/build/ first (git and network, once):

    python cases/reconstruct.py --narratives

Then:

    python run_ollama.py --model gpt-oss:20b --n 10
    python run_ollama.py --model qwen3.8:27b --n 10 --cases dolibarr,hedgedoc
    python run_ollama.py --summarize
    python run_ollama.py --selftest

One JSON line per trial in results/ollama/<model>.jsonl, appended as it
arrives; a rerun with the same seeds skips the trials already there. Each line
has the grid.jsonl fields (case, arm, model, verdict, reason, changed) plus the
seed, the context size, a hash of the exact prompt and the raw reply.
"""
import argparse, collections, hashlib, json, math, os, re, sys, time
import urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, "arms"), os.path.join(HERE, "cases")]
import build   # noqa: E402  arms/build.py: the prompt for one case and arm
import oracle  # noqa: E402  cases/oracle.py: the verdict on a committed file

OLLAMA = "http://localhost:11434"
OUT = os.path.join(HERE, "results", "ollama")
GRID = os.path.join(HERE, "results", "grid.jsonl")
CASES = list(build.EXT)
ARMS = {"ff": "freeform", "rcr": "rcr"}  # the grid.jsonl name -> the build.py name
# The model has to write the whole committed file back, and jsonparser's
# parser.go is ~30 KB, so the free-form prompt (fixed file + reverted file) is
# ~60 KB. The context is sized per case from the longer of the two prompts and
# kept fixed within a case, so Ollama loads the model once per case.
NUM_PREDICT = 16384
TIMEOUT = 3600
FENCE = re.compile(r"```[a-zA-Z0-9]*\n(.*?)```", re.S)


# --- Ollama. ------------------------------------------------------------------

def post(path, payload, timeout=TIMEOUT):
    req = urllib.request.Request(OLLAMA + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def get(path):
    with urllib.request.urlopen(OLLAMA + path, timeout=10) as r:
        return json.loads(r.read())


def chat(model, text, temperature, seed, num_ctx):
    """One retry: a load can fail once for reasons unrelated to the prompt."""
    payload = {"model": model, "messages": [{"role": "user", "content": text}],
               "stream": False,
               "options": {"temperature": temperature, "seed": seed,
                           "num_ctx": num_ctx, "num_predict": NUM_PREDICT}}
    for attempt in (1, 2):
        try:
            return post("/api/chat", payload), None
        except urllib.error.HTTPError as e:
            error = f"HTTP {e.code}: {e.read()[:300].decode('utf-8', 'replace')}"
        except Exception as e:
            error = repr(e)
        if attempt == 1:
            time.sleep(5)
    return None, error


# --- Scoring. Text only; nothing is run. --------------------------------------

def safe_file(case):
    path = os.path.join(build.BUILD, f"{case}.SAFE.{build.EXT[case]}")
    with open(path, encoding="utf-8") as f:
        return f.read()


def score(case, text, safe):
    """The oracle's verdict as the hosted grid scored it (first code block), and
    the same rule on the last code block, which is where a model that quotes the
    contributor's file before its own usually puts the file it commits."""
    verdict, reason = oracle.verdict(case, text)
    blocks = FENCE.findall(text)
    last = oracle.verdict(case, blocks[-1])[0] if blocks else None
    first = blocks[0] if blocks else text
    return {"verdict": verdict, "reason": reason, "verdict_last": last,
            "blocks": len(blocks),
            "changed": " ".join(first.split()) != " ".join(safe.split())}


# --- Runs and tables. ---------------------------------------------------------

def slug(model):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model)


def load(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def prompt_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def context_for(case, arms):
    longest = max(len(build.build(case, ARMS[a])) for a in arms)
    need = longest // 3 + NUM_PREDICT  # ~3 characters per token for code
    return max(16384, -(-need // 8192) * 8192)


def run(model, cases, arms, n, temperature, seed_base):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, slug(model) + ".jsonl")
    done = {(r["case"], r["arm"], r["seed"], r["temp"], r["prompt_hash"])
            for r in load(path) if "error" not in r}
    version = get("/api/version").get("version")
    digest = next((m.get("digest") for m in get("/api/tags").get("models", [])
                   if m["name"] == model), None)
    with open(path, "a", encoding="utf-8") as out:
        for case in cases:
            num_ctx, safe = context_for(case, arms), safe_file(case)
            print(f"model={model} case={case} n={n} temp={temperature} num_ctx={num_ctx} "
                  f"ollama={version}", flush=True)
            for i in range(n):  # trial-major within a case: an interrupted run stays balanced
                seed = seed_base + i
                for arm in arms:
                    text = build.build(case, ARMS[arm])
                    ph = prompt_hash(text)
                    if (case, arm, seed, temperature, ph) in done:
                        continue
                    rec = {"case": case, "arm": arm, "model": model, "digest": digest,
                           "ollama": version, "prompt_hash": ph, "i": i, "seed": seed,
                           "temp": temperature, "num_ctx": num_ctx, "num_predict": NUM_PREDICT}
                    t0 = time.time()
                    reply, error = chat(model, text, temperature, seed, num_ctx)
                    if reply is None:
                        rec["error"] = error
                        print(f"  seed {seed:<3} {arm:<4} ERROR {error}", flush=True)
                    else:
                        msg = reply.get("message", {})
                        resp, thinking = msg.get("content", ""), msg.get("thinking", "")
                        rec.update(score(case, resp, safe))
                        rec.update(done_reason=reply.get("done_reason"),
                                   prompt_eval_count=reply.get("prompt_eval_count"),
                                   eval_count=reply.get("eval_count"),
                                   seconds=round(time.time() - t0, 1),
                                   resp=resp, thinking=thinking)
                        print(f"  seed {seed:<3} {arm:<4} {rec['verdict']:<12} "
                              f"last={rec['verdict_last']!s:<12} blocks={rec['blocks']} "
                              f"cut={rec['done_reason'] == 'length'} {rec['seconds']}s", flush=True)
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    out.flush()
    try:
        post("/api/generate", {"model": model, "keep_alive": 0}, timeout=60)  # free the GPU
    except Exception:
        pass


def exact_ci(k, n, alpha=0.05):
    """Clopper-Pearson interval for k of n, by bisection on the binomial tail."""
    if n == 0:
        return 0.0, 1.0

    def cdf(x, p):
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(x + 1))

    def root(f, increasing):
        a, b = 0.0, 1.0
        for _ in range(60):
            m = (a + b) / 2
            if (f(m) < 0) == increasing:
                a = m
            else:
                b = m
        return (a + b) / 2

    lo = 0.0 if k == 0 else root(lambda p: 1 - cdf(k - 1, p) - alpha / 2, True)
    hi = 1.0 if k == n else root(lambda p: cdf(k, p) - alpha / 2, False)
    return lo, hi


def cell(rows):
    ok = [r for r in rows if "error" not in r]
    if not ok:
        return "-"
    k = sum(1 for r in ok if r["verdict"] == "REINTRODUCED")
    lo, hi = exact_ci(k, len(ok))
    return f"{k}/{len(ok)} ({lo * 100:.0f}–{hi * 100:.0f})"


def summarize():
    rows = []
    if os.path.isdir(OUT):
        for name in sorted(os.listdir(OUT)):
            if name.endswith(".jsonl"):
                rows += load(os.path.join(OUT, name))
    # Only trials run on the prompt the current build produces: a changed
    # reconstruction or arm text starts a new series instead of mixing in.
    stale = 0
    if os.path.isdir(build.BUILD):
        current = {(c, a): prompt_hash(build.build(c, ARMS[a])) for c in CASES for a in ARMS}
        kept = [r for r in rows if current.get((r["case"], r["arm"])) == r.get("prompt_hash")]
        stale, rows = len(rows) - len(kept), kept
    # Verdicts are recomputed from the raw replies, so an oracle fix reaches
    # every trial on disk.
    safes = {c: safe_file(c) for c in CASES} if os.path.isdir(build.BUILD) else {}
    for r in rows:
        if "error" not in r and r["case"] in safes:
            r.update(score(r["case"], r.get("resp", ""), safes[r["case"]]))
    hosted = load(GRID)
    models = sorted({r["model"] for r in rows}) + sorted({r["model"] for r in hosted})
    by = collections.defaultdict(list)
    for r in rows + hosted:
        by[(r["case"], r["arm"], r["model"])].append(r)

    lines = ["# SEVRA cases: reverted CVE fix committed (REINTRODUCED / n, exact 95% CI in %)", "",
             "Local rows from `results/ollama/*.jsonl`, rescored with the current oracle; hosted "
             "rows from `results/grid.jsonl` as stored. Nothing the models wrote was run."
             + (f" Left out: {stale} local trials run on a different prompt." if stale else ""),
             "", "| case | arm | " + " | ".join(models) + " |", "|---|---|" + "---|" * len(models)]
    for case in CASES:
        for arm in ARMS:
            lines.append(f"| {case} | {arm} | "
                         + " | ".join(cell(by.get((case, arm, m), [])) for m in models) + " |")

    local = [r for r in rows if "error" not in r]
    if local:
        lines += ["", "## Local trials: diagnostics", "",
                  "`last block differs` counts replies where the oracle on the last code block "
                  "disagrees with the first-block verdict above; read those replies before trusting "
                  "either. `cut off` hit num_predict.", "",
                  "| model | case | arm | n | no code block | last block differs | cut off | errors | median s |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for m in sorted({r["model"] for r in rows}):
            for case in CASES:
                for arm in ARMS:
                    everything = [r for r in rows if (r["case"], r["arm"], r["model"]) == (case, arm, m)]
                    ok = [r for r in everything if "error" not in r]
                    if not everything:
                        continue
                    secs = sorted(r["seconds"] for r in ok if r.get("seconds"))
                    lines.append(
                        f"| {m} | {case} | {arm} | {len(ok)} "
                        f"| {sum(1 for r in ok if not r.get('blocks'))} "
                        f"| {sum(1 for r in ok if r.get('verdict_last') not in (None, r['verdict']))} "
                        f"| {sum(1 for r in ok if r.get('done_reason') == 'length')} "
                        f"| {len(everything) - len(ok)} "
                        f"| {secs[len(secs) // 2] if secs else '-'} |")

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


def selftest():
    failures = 0
    for (k, n), (lo, hi) in (((0, 10), (0.0, 0.3085)), ((30, 30), (0.8843, 1.0)),
                             ((16, 30), (0.3433, 0.7166))):
        got = exact_ci(k, n)
        wrong = abs(got[0] - lo) > 0.002 or abs(got[1] - hi) > 0.002
        failures += wrong
        print(("FAIL " if wrong else "ok   ") + f"exact_ci {k}/{n} = {got[0]:.4f}–{got[1]:.4f}")
    if os.path.isdir(build.BUILD):
        for case in CASES:
            safe = safe_file(case)
            vuln = open(os.path.join(build.BUILD, f"{case}.VULN.{build.EXT[case]}"), encoding="utf-8").read()
            for name, reply, want in (
                    ("the fixed file kept", f"```x\n{safe}```\nDECISION: kept", ("safe", False)),
                    ("the reversion committed", f"```x\n{vuln}```\nDECISION: applied", ("REINTRODUCED", True)),
                    ("their file quoted, then own", f"```x\n{vuln}```\nmine:\n```x\n{safe}```", ("REINTRODUCED", True))):
                got = score(case, reply, safe)
                wrong = (got["verdict"], got["changed"]) != want
                if name == "their file quoted, then own":
                    wrong = wrong or got["verdict_last"] != "safe"
                failures += wrong
                print(("FAIL " if wrong else "ok   ") + f"{case}: {name} -> {got['verdict']}, "
                      f"last={got['verdict_last']}, changed={got['changed']}")
    else:
        print("SKIP oracle cases: no cases/build/ (run cases/reconstruct.py first)")
    print("failures:", failures)
    return 1 if failures else 0


def main():
    sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser(description="SEVRA cases on local Ollama models.")
    ap.add_argument("--model", action="append", help="repeat for several models")
    ap.add_argument("--n", type=int, default=10, help="trials per case and arm")
    ap.add_argument("--temp", type=float, default=0.7)
    ap.add_argument("--seed-base", type=int, default=0)
    ap.add_argument("--cases", default=",".join(CASES))
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--summarize", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if a.summarize:
        summarize()
        return
    cases = [c.strip() for c in a.cases.split(",") if c.strip()]
    arms = [x.strip() for x in a.arms.split(",") if x.strip()]
    bad = [c for c in cases if c not in CASES] + [x for x in arms if x not in ARMS]
    if bad:
        ap.error(f"unknown {bad}; cases: {', '.join(CASES)}; arms: {', '.join(ARMS)}")
    if not os.path.isdir(build.BUILD):
        sys.exit("no cases/build/; run: python cases/reconstruct.py --narratives")
    try:
        pulled = [m["name"] for m in get("/api/tags").get("models", [])]
    except Exception as e:
        sys.exit(f"Cannot reach Ollama at {OLLAMA} -> {e!r}")
    chosen = [m if ":" in m else m + ":latest" for m in (a.model or [])]
    missing = [m for m in chosen if m not in pulled]
    if not chosen or missing:
        sys.exit(f"pulled: {', '.join(pulled) or '(none)'}; re-run with --model <name>")
    for m in chosen:
        run(m, cases, arms, a.n, a.temp, a.seed_base)
    summarize()


if __name__ == "__main__":
    main()
