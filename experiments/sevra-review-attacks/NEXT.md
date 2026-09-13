# Open items

Nothing here is run yet. Priority order.

1. **Enforced witness execution.** The RESULTS split (jsonparser reduces, the
   off-screen cases don't) says the prose recipient procedure is not enough for a
   weak model. Test a harness where step (4) is mandatory: the recipient must
   actually run its own witness before it may change anything. Candidate spec
   rule: "a claim that current behaviour is a bug obliges you to reproduce it
   first." Measure whether this closes dolibarr/hedgedoc on Haiku.

2. **Local models (Qwen, gpt-oss), both arms.** The paper's target population runs
   the best model that fits a consumer GPU. Run the 3 cases (free-form × rcr,
   ± enforced witness) on gpt-oss:20b and the current best consumer-GPU Qwen, plus
   the toy policy for continuity with `../weak-model-injection`. n=30. Budget: the
   real-CVE files are larger than the toy, so expect 2–4× the toy's per-answer time
   on qwen; schedule as an overnight batch. Ollama on the GPU box.

3. **Adaptive-CLAIM variations.** Vary where/how the false claim sits (CLAIM vs
   CONTROLS vs HOLDS; strong vs hedged phrasing) to map when RCR's verification
   step bites. Connects to `../weak-model-injection` issue #10 (a CONTROLS line
   that grants access is a second claim).

4. **Benign / utility subset.** Run genuine security fixes (SEVRA ships 347 benign
   ground-truth fixes) through the RCR arm to show the format doesn't just reject
   everything — report a utility number beside the safety number.

5. **Contamination control.** Report result vs vulnerability age and SEVRA
   `failed_by`; add an obscured/renamed variant to separate recognition from
   memorization. Matters most for local models.

6. **More cases / a second domain.** Extend beyond 3 cases within the scorable
   CWE set (78, 89, 94, 22, 352, 79, 862) so the conclusion is about the message
   format, not these three files.

7. **Exact SEVRA model.** SEVRA evaluated Claude Opus 4.7 (still callable as
   `claude-opus-4-7`); our frontier used 4.8. A direct-API run pinning 4.7 (~$6–10
   for 30 runs) would close the reproduction loop on both ends.
