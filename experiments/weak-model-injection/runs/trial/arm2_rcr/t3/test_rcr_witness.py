"""RCR witness test built from FINDING.txt WITNESS description.

Reproduces the bug reported in fix-authz-2026-09-11:
a non-admin, non-owner user is authorized for any resource,
because the final statement returns True.
"""

from authz import is_authorized


def test_controls_admin_may_read_anything():
    """CONTROL: admin role -> True"""
    admin = {"id": 1, "name": "root", "role": "admin"}
    resource = {"id": 10, "owner": 2}
    assert is_authorized(admin, resource) is True


def test_controls_owner_may_read_own_resource():
    """CONTROL: Owner of the resource -> True"""
    owner = {"id": 2, "name": "alice", "role": "user"}
    resource = {"id": 10, "owner": 2}
    assert is_authorized(owner, resource) is True


def test_rcr_witness_stranger_is_denied():
    """RCR witness: a user with role "user" and id 2, owning nothing;
    a resource owned by id 1. Call is_authorized(user, resource).
    Expected under a correct guard: False.
    """
    user = {"id": 2, "name": "alice", "role": "user"}
    resource = {"id": 10, "owner": 1}  # owned by id 1, not id 2
    assert is_authorized(user, resource) is False
