"""Verify the fix and that all controls pass.

This test verifies:
1. CONTROL: admin role -> True (admin may read anything)
2. CONTROL: Owner of resource -> True (owner may read own resource)
3. FINDING FIX: Non-authorized user -> False (stranger denied)
"""

from authz import is_authorized

# Test data from test_authz.py (CONTROLS that must keep passing)
ADMIN = {"id": 1, "name": "root", "role": "admin"}
ALICE = {"id": 2, "name": "alice", "role": "user"}
ALICE_DOC = {"id": 10, "owner": 2}

# The witness case from the finding (the bug case that was failing)
BOB = {"id": 3, "name": "bob", "role": "user"}

print("Testing CONTROLS (must remain True):")
result_admin = is_authorized(ADMIN, ALICE_DOC)
print(f"1. Admin may read anything: is_authorized(ADMIN, ALICE_DOC) = {result_admin}")
assert result_admin is True, "CONTROL FAILED: Admin should be able to read anything"

result_owner = is_authorized(ALICE, ALICE_DOC)
print(f"2. Owner may read own resource: is_authorized(ALICE, ALICE_DOC) = {result_owner}")
assert result_owner is True, "CONTROL FAILED: Owner should be able to read own resource"

print("\nTesting FINDING FIX (must now be False):")
result_stranger = is_authorized(BOB, ALICE_DOC)
print(f"3. Stranger is denied: is_authorized(BOB, ALICE_DOC) = {result_stranger}")
assert result_stranger is False, "FIX FAILED: Stranger should be denied"

print("\nAll tests passed! The fix is correct and controls are maintained.")
