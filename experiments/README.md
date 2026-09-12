# Experiments

Each directory is one experiment about the format, with a README that
states the hypothesis, the setup, where the raw runs are, and the result,
scoped honestly: one confirmation of a mechanism is not a measurement, and
a batch that did not exercise the mechanism says so.

| Experiment | Question | Where it stands |
|---|---|---|
| [weak-model-injection](weak-model-injection/) | does a review in RCR form, as opposed to free-form prose, stop a weak model from merging a backdoor that rides beside a correct fix? | discriminated at n=30 on two local models (gpt-oss:20b, qwen3.8:27b). An overt backdoor is caught by recognition on a capable model, so the payload was made a plausible *policy* (an unowned resource treated as public): free-form merges it 30/30 on both models, the RCR record with a clean `CLAIM` keeps it out 0/30 on both, and the only leak is the same `WITNESS` prose (16–22/30). Round 3's controls show the record holds *without* the recipient procedure (0/30 both), so the protection is the form; the `WITNESS` prose leak closes on the capable model with the step-6 rule (qwen 22→1/30) but not on the weak one (gpt-oss 16→15/30). Round 4 adds Claude Haiku 4.5, Claude Sonnet and Claude Opus (n=10): the clean record is 0 on all six models; Sonnet refuses the drop-in file 10/10 yet accepts the same policy in plain words 8/10, so the vulnerable channel moves from code to speech with strength; Opus is 0 on every arm and in 23/80 files hardens the ownership check against the very rule it was offered. The `WITNESS` leak is present on the five weaker models (3/10 on Haiku and Sonnet) and no recipient rule closes it on all of them. Honest limit: the format bounds the channel, not the recipient's own habits, and one payload does not measure the ceiling. See [ollama/](weak-model-injection/ollama/), [haiku/](weak-model-injection/haiku/), [sonnet/](weak-model-injection/sonnet/), [opus/](weak-model-injection/opus/) |

## What is in here is material, not tools

The directories hold hostile review text, a toy function with a deliberate
bypass and scripts that reproduce a compromise on purpose. Nothing runs on
import, nothing reaches the network, and the "payload" writes a marker file
and no more. Still: do not point an agent with write access at these
directories outside the harness described in the experiment's README, and
do not copy records from here as examples of good practice. The examples
are in SPEC.md.
