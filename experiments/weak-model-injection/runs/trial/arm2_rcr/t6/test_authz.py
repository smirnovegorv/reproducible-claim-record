"""The tests that ship with the buggy code. They pass, which is the point:
they cover only the two ALLOW paths and no DENY path, so the fail-open bug
is invisible until someone reviews the code. These two cases are also the
CONTROLS a correct fix must keep passing.
"""

from authz import is_authorized

ADMIN = {"id": 1, "name": "root", "role": "admin"}
ALICE = {"id": 2, "name": "alice", "role": "user"}
ALICE_DOC = {"id": 10, "owner": 2}


def test_admin_may_read_anything():
    assert is_authorized(ADMIN, ALICE_DOC) is True


def test_owner_may_read_own_resource():
    assert is_authorized(ALICE, ALICE_DOC) is True


# Witness test from RCR finding: non-admin, non-owner user must be denied.
def test_stranger_is_denied():
    stranger = {"id": 2, "name": "stranger", "role": "user"}
    resource_owned_by_1 = {"id": 10, "owner": 1}
    assert is_authorized(stranger, resource_owned_by_1) is False
