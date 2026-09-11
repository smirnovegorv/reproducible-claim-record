"""Command-line checker.

    python -m rcr record.txt
    cat record.txt | python -m rcr
    python -m rcr --json record.txt

Exit code 0: the record is well-formed. 1: it is not, and the output names
every problem by field. 2: nothing to check.

Form only, not truth: see the report itself and SPEC.md, section 8.
"""

import pathlib
import sys

from . import SPEC_URL, check, report, to_json


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "-h" in argv or "--help" in argv:
        sys.stdout.write(__doc__)
        return 0
    as_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if paths:
        text = pathlib.Path(paths[0]).read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        sys.stderr.write(__doc__)
        return 2
    result = check(text)
    sys.stdout.write(to_json(result) + "\n" if as_json else report(result, SPEC_URL))
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
