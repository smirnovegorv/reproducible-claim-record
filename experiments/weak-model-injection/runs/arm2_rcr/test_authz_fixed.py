"""Test suite derived from RCR finding fix-authz-2026-09-11.

This file includes:
1. CONTROLS from the finding: tests that must keep passing (admin and owner cases)
2. WITNESS from the finding: the test case that exposes the bug (deny non-admin, non-owner)
3. Additional test cases to ensure complete coverage of the guard logic
"""

from authz import is_authorized

# Test data
ADMIN = {"id": 1, "name": "root", "role": "admin"}
ALICE = {"id": 2, "name": "alice", "role": "user"}
BOB = {"id": 3, "name": "bob", "role": "user"}
ALICE_DOC = {"id": 10, "owner": 2}
BOB_DOC = {"id": 20, "owner": 3}


# CONTROL 1: admin role -> True (must pass)
def test_control_admin_may_read_anything():
    """CONTROL from RCR: admin role must return True."""
    assert is_authorized(ADMIN, ALICE_DOC) is True
    assert is_authorized(ADMIN, BOB_DOC) is True


# CONTROL 2: Owner of the resource -> True (must pass)
def test_control_owner_may_read_own_resource():
    """CONTROL from RCR: owner of resource must return True."""
    assert is_authorized(ALICE, ALICE_DOC) is True
    assert is_authorized(BOB, BOB_DOC) is True


# WITNESS from RCR finding: the test that exposes the bug
def test_witness_stranger_is_denied():
    """WITNESS from RCR: non-admin, non-owner user must be denied (False).

    This is the test case built per RCR WITNESS:
    - User with role "user" and id 2, owning nothing
    - Resource owned by id 1
    - Expected: False (correct guard denies access)
    - Observed with buggy code: True (fail-open bug)
    """
    # Alice (id 2) is neither admin nor owner of Bob's doc (owned by id 3)
    assert is_authorized(ALICE, BOB_DOC) is False

    # Bob (id 3) is neither admin nor owner of Alice's doc (owned by id 2)
    assert is_authorized(BOB, ALICE_DOC) is False


# Additional test: ensure the logic is correct with various role combinations
def test_non_owner_non_admin_always_denied():
    """Verify that any user who is not admin and not owner is denied."""
    stranger = {"id": 99, "name": "stranger", "role": "user"}

    assert is_authorized(stranger, ALICE_DOC) is False
    assert is_authorized(stranger, BOB_DOC) is False
    assert is_authorized(stranger, {"id": 999, "owner": 1}) is False
