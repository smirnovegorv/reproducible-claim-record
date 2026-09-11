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


# Missing, and the whole bug: no test that a stranger is DENIED.
def test_stranger_is_denied():
    """Witness from RCR finding: non-admin, non-owner user should be denied.
    A user with role 'user' and id 2, owning nothing;
    a resource owned by id 1. Expected: False. Bug returns: True."""
    stranger = {"id": 3, "name": "bob", "role": "user"}
    resource_owned_by_alice = {"id": 10, "owner": 2}
    assert is_authorized(stranger, resource_owned_by_alice) is False
