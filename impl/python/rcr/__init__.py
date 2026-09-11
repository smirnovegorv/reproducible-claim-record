"""RCR, Reproducible Claim Record: the reference implementation.

`import rcr` gives the checker from `rcr.core` (one file, standard library
only, meant to be copied as it is) and the two texts bundled with the
package: the specification and the short skill file for agents.

The checker verifies form, not truth and not safety. What to do with a
record is decided by the recipient, on the recipient's side, by the
procedure in the specification.
"""

from importlib import resources

from .core import *  # noqa: F401,F403 — the public surface named in SPEC.md
from .core import (  # explicit, so that editors and readers see the surface
    Problem, Record, Result,
    extract, parse, validate, detect, check, report, to_json,
    VERSION, VERSIONS, LEGACY_VERSIONS, KINDS, MAX_BYTES,
    RECORD_LABELS, RECEIPT_LABELS, REQUIRED, ENUMS, VERIFIED_PREFIXES,
    CODE_MARKS, URL_ALLOWED,
)

__version__ = "0.3.0"
SPEC_URL = "https://foragents.site/rcr.md"


def _data(name: str) -> str:
    return resources.files(__package__).joinpath("data", name).read_text(encoding="utf-8")


def spec_text() -> str:
    """SPEC.md as bundled with this version of the package."""
    return _data("SPEC.md")


def skill_text() -> str:
    """The short form for agents, as bundled with this version."""
    return _data("SKILL.md")


__all__ = [
    "Problem", "Record", "Result",
    "extract", "parse", "validate", "detect", "check", "report", "to_json",
    "VERSION", "VERSIONS", "LEGACY_VERSIONS", "KINDS", "MAX_BYTES",
    "RECORD_LABELS", "RECEIPT_LABELS", "REQUIRED", "ENUMS", "VERIFIED_PREFIXES",
    "CODE_MARKS", "URL_ALLOWED",
    "SPEC_URL", "spec_text", "skill_text", "__version__",
]
