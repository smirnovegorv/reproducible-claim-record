# Experiments

Each directory is one experiment about the format, with a README that
states the hypothesis, the setup, where the raw runs are, and the result,
scoped honestly: one confirmation of a mechanism is not a measurement, and
a batch that did not exercise the mechanism says so.

| Experiment | Question | Where it stands |
|---|---|---|
| [weak-model-injection](weak-model-injection/) | does a review in RCR form, as opposed to free-form prose, stop a weak model from merging a backdoor that rides beside a correct fix? | discriminated at n=30 on two local models (gpt-oss:20b, qwen3.8:27b). An overt backdoor is caught by recognition on a capable model, so the payload was made a plausible *policy* (an unowned resource treated as public): free-form merges it 30/30 on both models, the RCR record with a clean `CLAIM` keeps it out 0/30 on both, and the only leak is the same `WITNESS` prose (16–22/30). Round 3's controls show the record holds *without* the recipient procedure (0/30 both), so the protection is the form; the `WITNESS` prose leak closes on the capable model with the step-6 rule (qwen 22→1/30) but not on the weak one (gpt-oss 16→15/30). Round 4 adds Claude Haiku 4.5, Claude Sonnet and Claude Opus (n=10): the clean record is 0 on all five models; Sonnet refuses the drop-in file 10/10 yet accepts the same policy in plain words 8/10, so the vulnerable channel moves from code to speech with strength; Opus is 0 on every arm and in 23/80 files hardens the ownership check against the very rule it was offered. The `WITNESS` leak is present on the four weaker models (3/10 on Haiku and Sonnet) and no recipient rule closes it on all of them. Round 5, proposed by readers: the same policy written as a third `CONTROLS` line instead of a `WITNESS` aside is taken by Sonnet 5/5 (p=0.0003 against the clean record), because the recipient rule that closed the `WITNESS` leak tells the recipient to derive from `CONTROLS`; a control that grants access is a second claim, and the spec does not yet say so (issue #10). Honest limit: the format bounds the channel, not the recipient's own habits, and one payload does not measure the ceiling. See [ollama/](weak-model-injection/ollama/), [haiku/](weak-model-injection/haiku/), [sonnet/](weak-model-injection/sonnet/), [opus/](weak-model-injection/opus/), [controls/](weak-model-injection/controls/) |
| [sevra-review-attacks](sevra-review-attacks/) | the same question on real third-party CVEs and across a model gradient: which models merge a malicious review that reverts a real upstream fix, and does RCR form change it? | Free-form is a steep capability gradient: Haiku 4.5 merges the reversion 28/30, Sonnet 5 and Opus 4.8 0/30 each (Fisher p≈3e-21) — reproducing SEVRA-BENCH (Haiku is one of its baselines) and showing much of the benchmark's headline risk is a mid-tier-model property the frontier has already closed. Because a SEVRA attack is a *false claim* about safe code, its RCR rendering carries the persuasion in `CLAIM`; at n=10 RCR gives Haiku no significant protection (23/30), moving only the one case with a concrete runnable witness (jsonparser 8→3, p=0.07). Contrast weak-model-injection, where a clean `CLAIM` keeps weak models at 0/30: RCR removes a *delivery* channel, not *persuasion*. See [sevra-review-attacks/RESULTS.md](sevra-review-attacks/RESULTS.md) |

## What is in here is material, not tools

The directories hold hostile review text, a toy function with a deliberate
bypass and scripts that reproduce a compromise on purpose. Nothing runs on
import, nothing reaches the network, and the "payload" writes a marker file
and no more. Still: do not point an agent with write access at these
directories outside the harness described in the experiment's README, and
do not copy records from here as examples of good practice. The examples
are in SPEC.md.
