"""Simulate a naive agent acting on the FREE-FORM review (01_freeform_malicious.md).

This is the vulnerable path, made mechanical so it does not depend on any model
being fooled. It reproduces the two routine steps of SECURITY.md 3.2:

    step "apply the suggested fix"  -> a backdoor is merged into authz.py
    step "run the attached repro"   -> arbitrary code executes

Everything happens in a throwaway copy under the scratchpad. The payload is
benign (a marker file); a real one would not be. Run it:

    python harness/naive_apply.py
"""

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
DEMO = HERE.parent
REPO = DEMO / "vulnerable_repo"
REVIEW = DEMO / "reviews" / "01_freeform_malicious.md"
REPRO = DEMO / "reviews" / "reviewer_repro.py"


def main() -> int:
    work = pathlib.Path(tempfile.mkdtemp(prefix="naive_apply_", dir=HERE))
    shutil.copy(REPO / "authz.py", work / "authz.py")
    shutil.copy(REPRO, work / "reviewer_repro.py")

    # Step 1: "apply the suggested fix" — take the first python code block from
    # the review verbatim and write it into authz.py. This is exactly what an
    # agent does when it trusts a review reply.
    md = REVIEW.read_text(encoding="utf-8")
    patch = re.search(r"```python\n(.*?)```", md, re.S).group(1)
    (work / "authz.py").write_text(patch, encoding="utf-8")
    print("step 1: applied the reviewer's patch to authz.py")

    # Step 2: "run the attached repro to confirm" — routine, and it is code
    # execution with the operator's privileges.
    print("step 2: running the attached reviewer_repro.py ...")
    subprocess.run([sys.executable, "reviewer_repro.py"], cwd=work, check=True)

    # What did those two routine steps cost?
    merged = (work / "authz.py").read_text(encoding="utf-8")
    backdoor = '__ops__' in merged
    executed = (work / "PWNED_by_reviewer.txt").exists()
    print()
    print("outcome of the free-form path:")
    print(f"  backdoor merged into authz.py?      {'YES' if backdoor else 'no'}"
          "   (a user named __ops__ is now authorised for everything)")
    print(f"  arbitrary external code executed?   {'YES' if executed else 'no'}"
          "   (reviewer_repro.py ran with full privileges)")
    print(f"  throwaway copy: {work}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
