"""Test for RCR finding fix-authz-2026-09-11.
Built following RCR procedure: recreate the witness from WITNESS description.
"""

from authz import is_authorized


def test_non_admin_non_owner_is_denied():
    """A user with role 'user' and id 2, owning nothing, accessing a resource owned by id 1.

    Expected: False (access denied)
    Bug observed: True (fail-open)
    """
    user = {"id": 2, "name": "alice", "role": "user"}
    resource = {"id": 10, "owner": 1}  # owned by different user
    assert is_authorized(user, resource) is False
