"""Regenerate the SAFE and VULN versions of each case file from PUBLIC commits.

No vulnerable source is stored in this repository. For each case in manifest.json
this script:
  1. downloads the fixed file at the fixing commit  -> build/<case>.SAFE.<ext>
  2. downloads that commit's .patch and reverse-applies the hunks touching the
     target file (git apply -R) -> build/<case>.VULN.<ext>  (the pre-fix, vulnerable file)
  3. optionally fetches the SEVRA review narrative (by vuln_id + framing) into
     build/<case>.narrative.txt, used by ../arms/build.py for the free-form arm.

Requires: git on PATH, network access to github.com (and, for --narratives,
datasets-server.huggingface.co). Everything lands in build/, which is gitignored.

    python reconstruct.py            # SAFE + VULN for every case
    python reconstruct.py --narratives   # also fetch SEVRA narratives
"""
import json
import os
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
EXT = {"dolibarr": "php", "hedgedoc": "js", "jsonparser": "go"}


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "rcr-reconstruct"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def _raw_url(repo, commit, path):
    owner_repo = repo.rstrip("/").split("github.com/")[-1]
    return f"https://raw.githubusercontent.com/{owner_repo}/{commit}/{path}"


def reconstruct(case, narratives=False):
    name, repo, commit, path = case["name"], case["repo"], case["fix_commit"], case["file"]
    ext = EXT[name]
    os.makedirs(BUILD, exist_ok=True)
    safe = _get(_raw_url(repo, commit, path)).decode("utf-8", "replace")
    safe = safe.replace("\r\n", "\n")
    open(os.path.join(BUILD, f"{name}.SAFE.{ext}"), "w", encoding="utf-8", newline="\n").write(safe)

    patch = _get(f"{repo.rstrip('/')}/commit/{commit}.patch").decode("utf-8", "replace")
    with tempfile.TemporaryDirectory() as td:
        tgt = os.path.join(td, path)
        os.makedirs(os.path.dirname(tgt), exist_ok=True)
        open(tgt, "w", encoding="utf-8", newline="\n").write(safe)
        pf = os.path.join(td, "fix.patch")
        open(pf, "w", encoding="utf-8", newline="\n").write(patch)
        subprocess.run(["git", "init", "-q"], cwd=td, check=True)
        subprocess.run(["git", "add", "-A"], cwd=td, check=True)
        subprocess.run(["git", "-c", "user.email=a@b.c", "-c", "user.name=x",
                        "commit", "-qm", "safe"], cwd=td, check=True)
        # reverse only the hunks that touch the target file -> the vulnerable version
        subprocess.run(["git", "apply", "-R", "--include", path, "--recount", pf],
                       cwd=td, check=True)
        vuln = open(tgt, encoding="utf-8").read().replace("\r\n", "\n")
    open(os.path.join(BUILD, f"{name}.VULN.{ext}"), "w", encoding="utf-8", newline="\n").write(vuln)
    assert vuln != safe, f"{name}: reverse-apply produced no change"
    print(f"  {name}: SAFE {len(safe)}b, VULN {len(vuln)}b")

    if narratives:
        _fetch_narrative(case)


def _fetch_narrative(case):
    """Best-effort SEVRA narrative fetch by vuln_id + framing via datasets-server."""
    name = case["name"]
    vid = case["vuln_id"].split(" ")[0].split("/")[0]
    framing = case["sevra_framing"]
    # scan the malicious split of each cwe config for a row matching vuln_id+axis3
    import re
    cwe = re.search(r"CWE-(\d+)", case["cwe"]).group(1)
    base = ("https://datasets-server.huggingface.co/rows?dataset=RedAI4Code/SEVRA"
            f"&config=cwe{cwe}-deterministic&split=malicious")
    for off in range(0, 400, 100):
        try:
            d = json.loads(_get(base + f"&offset={off}&length=100"))
        except Exception as e:
            print(f"  {name}: narrative fetch failed ({e}); supply build/{name}.narrative.txt manually")
            return
        for r in d.get("rows", []):
            row = r["row"]
            if row.get("vuln_id", "").startswith(vid) and row.get("axis3") == framing:
                text = f"{row['pr_title']}\n\n{row['pr_body']}".replace("\r\n", "\n").strip()
                open(os.path.join(BUILD, f"{name}.narrative.txt"), "w",
                     encoding="utf-8", newline="\n").write(text)
                print(f"  {name}: narrative ({framing}) saved")
                return
        if off >= d.get("num_rows_total", 0):
            break
    print(f"  {name}: no SEVRA row for {vid}/{framing}; supply build/{name}.narrative.txt manually")


def main():
    manifest = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))
    narratives = "--narratives" in sys.argv
    for case in manifest["cases"]:
        reconstruct(case, narratives=narratives)
    print("done -> build/  (gitignored)")


if __name__ == "__main__":
    main()
