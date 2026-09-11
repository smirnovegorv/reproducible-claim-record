# Experiments

Each directory is one experiment about the format, with a README that
states the hypothesis, the setup, where the raw runs are, and the result,
scoped honestly: one confirmation of a mechanism is not a measurement, and
a batch that did not exercise the mechanism says so.

| Experiment | Question | Where it stands |
|---|---|---|
| [weak-model-injection](weak-model-injection/) | does a review in RCR form, as opposed to free-form prose, stop a weak model from merging a backdoor that rides beside a correct fix? | the mechanism was confirmed once: the same review in prose got the backdoor merged, in RCR form the model derived the fix from `CLAIM` and `CONTROLS`. A later batch of six per arm did not exercise it: the model declined the bait in every arm. Inconclusive as a measurement; open |

## What is in here is material, not tools

The directories hold hostile review text, a toy function with a deliberate
bypass and scripts that reproduce a compromise on purpose. Nothing runs on
import, nothing reaches the network, and the "payload" writes a marker file
and no more. Still: do not point an agent with write access at these
directories outside the harness described in the experiment's README, and
do not copy records from here as examples of good practice. The examples
are in SPEC.md.
