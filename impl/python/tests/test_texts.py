"""The bundled texts equal the repository's, and the specification names
everything the checker knows: every code, label, value, prefix and flag."""

import pathlib
import re

import rcr

ROOT = pathlib.Path(__file__).resolve().parents[3]
CORE = ROOT / "impl/python/rcr/core.py"


def _spec():
    return (ROOT / "SPEC.md").read_text(encoding="utf-8")


def test_bundled_spec_equals_the_repository_spec():
    assert rcr.spec_text() == _spec(), "impl/python/rcr/data/SPEC.md drifted from SPEC.md"


def test_bundled_skill_equals_the_repository_skill():
    repo = (ROOT / "integrations/skill/SKILL.md").read_text(encoding="utf-8")
    assert rcr.skill_text() == repo, "impl/python/rcr/data/SKILL.md drifted"


def test_spec_names_the_version_the_package_implements():
    assert f"Reproducible Claim Record, {rcr.VERSION}" in _spec()
    assert rcr.__version__.startswith(rcr.VERSION + ".")


def _codes_in_core():
    source = CORE.read_text(encoding="utf-8")
    return set(re.findall(r'Problem\(\s*[^,]+,\s*"([a-z_]+)"', source))


def _codes_in_spec():
    spec = _spec()
    section = spec[spec.index("## 12. Diagnostics"):]
    return {line[3:line.index("`", 3)] for line in section.splitlines()
            if line.startswith("| `")}


def test_section_12_lists_exactly_the_codes_the_checker_emits():
    """A code the text does not name is a surprise; a code the checker never
    emits is a promise nobody keeps."""
    assert _codes_in_core() == _codes_in_spec(), (
        _codes_in_core() ^ _codes_in_spec())


def test_spec_names_every_rule_the_checker_enforces():
    spec = _spec()
    for label in rcr.RECORD_LABELS + rcr.RECEIPT_LABELS:
        assert label in spec, label
    for values in rcr.ENUMS.values():
        for value in values:
            assert value in spec, value
    for prefix in rcr.VERIFIED_PREFIXES:
        assert prefix in spec, prefix
    for mark, _ in rcr.CODE_MARKS:
        if mark != "<script":
            assert mark in spec, mark
    for flag in ("demands_execution", "replacement_value", "origin_url_only",
                 "author_reported_only"):
        assert flag in spec, flag
    for name in ("extract(text)", "parse(text)", "validate(record)", "detect(record)",
                 "check(text)", "report(result, spec_url)"):
        assert name in spec, name


def test_spec_names_the_roles_and_states():
    spec = _spec()
    assert "### Terms" in spec
    for role in ("Operator", "Owner", "Finder", "Reproducer", "Origin",
                 "Affected", "Checker"):
        assert f"**{role}**" in spec, role
    for state in ("**closed**", "**confirmed**", "**verified**"):
        assert state in spec, state
    assert "A verdict is not a permission" in spec


def test_spec_carries_no_dates_and_no_board_history():
    """The text is read on other people's boards; its history lives in docs/."""
    spec = _spec()
    assert not re.search(r"\b20\d\d-\d\d-\d\d\b", spec)
    assert "seq " not in spec and "Tavern" not in spec
