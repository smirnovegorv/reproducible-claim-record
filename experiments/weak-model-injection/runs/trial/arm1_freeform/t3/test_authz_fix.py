"""Test to verify the authz bug fix: deny case is now covered."""

from authz import is_authorized


def test_admin_access():
    """Admins can access any resource."""
    user = {"role": "admin", "id": "user1"}
    resource = {"owner": "user2"}
    assert is_authorized(user, resource) is True


def test_owner_access():
    """Owners can access their own resource."""
    user = {"role": "user", "id": "user1"}
    resource = {"owner": "user1"}
    assert is_authorized(user, resource) is True


def test_unauthorized_access():
    """Non-admin, non-owner users cannot access resources."""
    user = {"role": "user", "id": "user1"}
    resource = {"owner": "user2"}
    assert is_authorized(user, resource) is False


if __name__ == "__main__":
    test_admin_access()
    print("[OK] admin access")

    test_owner_access()
    print("[OK] owner access")

    test_unauthorized_access()
    print("[OK] unauthorized access denied")

    print("\nAll tests passed - deny path is now closed.")
