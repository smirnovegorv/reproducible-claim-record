# Reference implementation, Python

One file, [rcr/core.py](rcr/core.py), with no dependencies outside the
standard library, packaged so that it can be installed and run; the file
alone can also be copied into any project as it is.

Implements SPEC.md version 0.3 and reads records marked 0.1 and 0.2.

```
pip install "reproducible-claim-record @ git+https://github.com/smirnovegorv/reproducible-claim-record.git#subdirectory=impl/python"
python -m rcr record.txt          # exit 0 well-formed, 1 not, 2 nothing to check
python -m rcr --json record.txt   # the structure from SPEC.md section 12
```

From Python the surface is the one named in SPEC.md section 10:
`extract`, `parse`, `validate`, `detect`, `check`, `report`, `to_json`,
and `Record.to_dict()`. The package also bundles the texts it was built
against: `rcr.spec_text()` and `rcr.skill_text()`, equal to `SPEC.md` and
`integrations/skill/SKILL.md` at the same commit; a test holds that.

## Tests

```
pip install -e ".[test]"
pytest
```

`tests/test_rcr.py` holds the rules one by one; `tests/test_conformance.py`
runs the corpus in `../../conformance/`; `tests/test_texts.py` holds the
bundled texts and the specification together with the code: every code the
checker emits is in section 12, every label, value and flag it knows is in
the text.

Comments inside `core.py` are in Russian and carry the history of each rule.
The specification, not the code, is the contract.
