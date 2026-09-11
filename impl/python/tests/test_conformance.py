"""The reference implementation passes the corpus every implementation must.

Each case is a record in conformance/cases/<name>.rcr and its expectation
in <name>.json: ok, kind, version, the (field, code) pairs of the problems
as a set, and the flags. Text of messages is not compared: it is the
implementation's own.
"""

import json
import pathlib

import pytest

import rcr

ROOT = pathlib.Path(__file__).resolve().parents[3]
CASES = ROOT / "conformance" / "cases"
EXTRACT = ROOT / "conformance" / "extract"


def _cases(folder, suffix):
    files = sorted(folder.glob(f"*{suffix}"))
    assert files, folder
    return [pytest.param(f, id=f.stem) for f in files]


@pytest.mark.parametrize("path", _cases(CASES, ".rcr"))
def test_case(path):
    expected = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
    result = rcr.check(path.read_text(encoding="utf-8"))
    got = {
        "ok": result.ok,
        "kind": result.kind,
        "version": result.version,
        "problems": sorted({(p.field, p.code) for p in result.problems}),
        "flags": sorted(set(result.flags)),
    }
    want = {
        "ok": expected["ok"],
        "kind": expected["kind"],
        "version": expected["version"],
        "problems": sorted({(p["field"], p["code"]) for p in expected["problems"]}),
        "flags": sorted(set(expected["flags"])),
    }
    assert got == want, [p.text for p in result.problems]


@pytest.mark.parametrize("path", _cases(EXTRACT, ".txt"))
def test_extract_case(path):
    expected = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
    blocks = rcr.extract(path.read_text(encoding="utf-8"))
    assert len(blocks) == expected["records"]
    ids = []
    for block in blocks:
        record, problems = rcr.parse(block)
        assert record is not None and not problems, problems
        ids.append(record.get("ID") or record.get("RECEIPT").split()[0])
    assert ids == expected["ids"]


def test_every_code_in_the_specification_has_a_case():
    """A code nobody can trigger is a code nobody can test against."""
    spec = (ROOT / "SPEC.md").read_text(encoding="utf-8")
    section = spec[spec.index("## 12. Diagnostics"):]
    codes = set()
    for line in section.splitlines():
        if line.startswith("| `") and "|" in line[3:]:
            codes.add(line[3:line.index("`", 3)])
    seen = set()
    for path in CASES.glob("*.json"):
        for p in json.loads(path.read_text(encoding="utf-8"))["problems"]:
            seen.add(p["code"])
    assert codes <= seen, sorted(codes - seen)
