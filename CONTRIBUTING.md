# Contributing

RCR is a specification first. Everything else here, the reference
implementation included, follows the text and never the other way round.

## Changing the specification

- Open an issue before a pull request. Name the rule, the record it gets
  wrong, and what the recipient would do differently under the change.
- **No rule without a case, no case without a rule.** A change to SPEC.md
  that adds, removes or tightens a rule comes with a record in
  `conformance/cases/` that fails under the old text and passes under the
  new one, or the reverse. A new case that no sentence of SPEC.md explains
  is not accepted.
- A change to the wording alone, for a reader who found the text unclear,
  needs no case. Say which sentence you could not follow and what you read
  instead; that is the whole review.
- The reference implementation is updated in the same pull request, and
  CHANGELOG.md gets a line.
- The specification carries no dates, no names and no history of the
  project it came from. Those belong in `docs/`.

A review of the specification itself may be sent as an RCR finding, with
`TARGET` naming `SPEC.md @ <commit>`. That is how the text has been
reviewed so far, and it is the fairest test of whether the format can
carry a review of prose.

## Adding an implementation

- One directory per language under `impl/`, with a README that says which
  version of SPEC.md it implements and how to run its tests.
- It must run the whole corpus in `conformance/` as part of its own tests,
  and report the codes from SPEC.md section 12. The wording of messages is
  the implementation's own.
- The reference implementation stays a single file with no dependencies
  outside the standard library. Other implementations are free to be
  idiomatic.

## Adding a tool

- One directory per tool under `tools/`, with a README that says what it
  does, which implementation it builds on, and what it needs to run.
- A tool reads records through the public surface named in SPEC.md
  section 10 and never reaches into the prose of a field with rules of its
  own. If a tool needs a rule the checker does not have, that is a change
  to the specification, above.

## Adding an experiment

- One directory per experiment under `experiments/`, with a README that
  states the hypothesis, the setup, the raw runs and the result, scoped
  honestly: one confirmation of a mechanism is not a measurement, and a
  batch that did not exercise the mechanism says so.
- Adversarial material (hostile reviews, toy backdoors) is kept inert:
  nothing in an experiment directory runs on import, and the README says
  what not to point an agent with write access at.

## Language

SPEC.md, READMEs and the corpus are in English. `docs/rationale.ru.md` is
in Russian and stays so; articles carry a language suffix in the filename.
Comments inside the reference implementation are in Russian, which is why
the specification and not the code is the contract.
