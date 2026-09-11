"""Test the authz fix independently."""
import sys
sys.path.insert(0, __file__[:__file__.rfind('\\')])

from authz import is_authorized

# Test admin access (should pass)
admin = {"role": "admin", "id": "a1", "name": "Alice"}
resource = {"owner": "b1", "name": "secret"}
assert is_authorized(admin, resource) is True, "Admin should be authorized"

# Test owner access (should pass)
owner = {"role": "user", "id": "b1", "name": "Bob"}
assert is_authorized(owner, resource) is True, "Owner should be authorized"

# Test unauthorized user (this was the bug - should now FAIL)
unauthorized = {"role": "user", "id": "c1", "name": "Charlie"}
assert is_authorized(unauthorized, resource) is False, "Unauthorized user should be denied"

print("All tests pass: deny path now works correctly")
