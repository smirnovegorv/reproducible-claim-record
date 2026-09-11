"""Comprehensive test suite for authz.py to validate the RCR finding and fix."""

from authz import is_authorized

ADMIN = {"id": 1, "name": "root", "role": "admin"}
ALICE = {"id": 2, "name": "alice", "role": "user"}
BOB = {"id": 3, "name": "bob", "role": "user"}
ALICE_DOC = {"id": 10, "owner": 2}


def test_admin_may_read_anything():
    """CONTROL: admin should always be authorized."""
    assert is_authorized(ADMIN, ALICE_DOC) is True


def test_owner_may_read_own_resource():
    """CONTROL: owner should be authorized for their own resource."""
    assert is_authorized(ALICE, ALICE_DOC) is True


def test_stranger_is_denied():
    """RCR finding witness: non-admin, non-owner user should be denied."""
    # This test will fail with the buggy code (returns True)
    # and pass after the fix (returns False)
    assert is_authorized(BOB, ALICE_DOC) is False
