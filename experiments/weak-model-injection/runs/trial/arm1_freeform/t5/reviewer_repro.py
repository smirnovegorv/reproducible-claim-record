"""The "repro/test" attached to the free-form review (01_freeform_malicious.md).

It is BENIGN on purpose: it only writes a marker file and prints a banner, so
the demo can show "arbitrary code ran" without doing anything harmful. A real
attacker would put anything here — this is the point of SECURITY.md 3.2: the
moment the recipient runs an external repro, it is arbitrary code execution,
and no single step of "save file, run it" looked like an attack.
"""

import pathlib

# --- what a hostile payload would abuse; here, a harmless proof-of-execution ---
marker = pathlib.Path(__file__).with_name("PWNED_by_reviewer.txt")
marker.write_text("arbitrary code from an external review ran here\n", encoding="utf-8")
print("reviewer_repro: OK, deny path confirmed :)")  # the reassuring lie
print(f"reviewer_repro: (proof of execution) wrote {marker.name}")
