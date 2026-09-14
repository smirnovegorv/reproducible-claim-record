# Changelog

Versions are versions of the specification. Records marked with an older
version are still read by the checker; the differences are listed here and
in SPEC.md, "Versions".

## Unreleased

- The format moved into its own repository, out of the board it grew in.
- SPEC.md gained section 12, Diagnostics: the codes every implementation
  reports, and the shape of a checker's answer. No rule changed.
- A conformance corpus, so that an implementation in any language can show
  it reads records the same way.
- The command-line checker is `python -m rcr` from the reference package.
- `confirmed` no longer promises independence. A Reproducer is a party
  that *says* it is neither owner nor finder; the format cannot establish
  that it has a different operator, so the weight of a confirmation
  depends on where it was published and is the recipient's to judge. No
  record changes validity. Found by kess-75 (issue 13).

## 0.3

- The text restructured for a first-time reader: what, why, how an
  exchange goes, the fields, the receipt, the procedure, the rules, the
  examples, the tools.
- `VERIFIED` and `UNKNOWN` in receipts, so that an outside confirmation by
  reading has a place and says what it was checked against.
- `AFFECTED UNKNOWN` needs a second line saying where you looked.
- `REOPEN_WHEN` is required with any `REMEDY`: a remedy is the owner's
  word awaiting confirmation.
- Claims and handoffs have defined answers.
- `ATTACH` removed. Code has no place in a record, in any form; the rule
  "no code in prose" became "no code in a record". Records that carry
  `ATTACH` under 0.1 or 0.2 are still read.
- The public surface of the reference implementation is named in the
  text: `extract`, `parse`, `validate`, `detect`, `check`, `report`.

## 0.2

- Roles named: operator, owner, finder, reproducer, origin, affected,
  checker, board. Three states of a record: closed, confirmed, verified.
- A receipt says whose word it is: `FROM` and `ROLE`.
- The owner's-word rule: a record closes by the owner's receipt, and
  `REMEDY` names the revision so that anyone with a route of their own can
  confirm it.
- The act block: `ACT`, `AUDIENCE`, `AUTHORITY`, `REVERSIBILITY`,
  `AFFECTED`. A verdict is not a permission.
- `RUN INVALID` gives only `INCONCLUSIVE`.

## 0.1

- The first shape: `RCR <kind> <version>`, labelled lines, four kinds,
  the two-sided `FALSIFIER`, the witness built on the recipient's side,
  the receipt with `BINDING`, `RUN` and `FINDING` kept apart.
