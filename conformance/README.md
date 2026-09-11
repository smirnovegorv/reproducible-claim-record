# Conformance corpus

The test every implementation of RCR has to pass, in any language. No code
here: records and the answers a checker must give.

## Layout

`cases/<name>.rcr` is one record, exactly as a checker would receive it.
`cases/<name>.json` is what the checker must say about it:

```
{
  "ok": false,
  "kind": "finding",
  "version": "0.3",
  "problems": [{"field": "VERIFIED", "code": "bad_prefix"}],
  "flags": []
}
```

- `ok`: whether the record is well-formed.
- `kind`, `version`: from the header line; `null` when there is no header
  or the record is over the size limit.
- `problems`: the field and the code of every problem, compared as a set:
  the order is not significant, a rule broken twice may be named once or
  twice, and the message text is not compared. Codes are the ones in
  SPEC.md section 12.
- `flags`: the flags, as a set. Empty whenever `problems` is not.

`extract/<name>.txt` is a longer text with records inside it, and
`extract/<name>.json` says how many records `extract` must find and their
identifiers in order.

Names say what the case is about: `ok_*` well-formed, `err_*` one rule
broken, `flag_*` well-formed with a flag, `pair_*` a legal or illegal
`RUN`, `FINDING` and `BINDING` combination from the table in SPEC.md
section 5.

## Running it

The reference implementation runs the corpus in
`impl/python/tests/test_conformance.py`. Another implementation runs it in
its own way: read each `.rcr`, compare with each `.json`.

## Adding a case

Every rule in SPEC.md has at least one case here, and every case here is
explained by a sentence in SPEC.md; a pull request that changes one changes
the other. The expectations were first produced by the reference
implementation and then read against the specification one by one; when
the two disagreed, the specification won and the implementation changed.
Where a rule has an obvious near miss (an identifier that looks like code,
a link in a field that allows one), the corpus holds the near miss too, so
that an implementation cannot pass by being stricter than the text.

Records here are synthetic or anonymised. Names, revisions and identifiers
in them refer to nothing.
