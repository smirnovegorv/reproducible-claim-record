"""Verify the bug found in the RCR finding.

Build the witness myself from the finding's WITNESS section:
- A user with role "user" and id 2, owning nothing
- A resource owned by id 1
- Call is_authorized(user, resource)
- Expected under correct guard: False
- Observed at buggy revision: True
"""

from authz import is_authorized

# The witness case from the finding
user = {"id": 2, "role": "user"}
resource = {"owner": 1}

result = is_authorized(user, resource)
print(f"is_authorized(user={user}, resource={resource}) = {result}")
print(f"Expected: False (user has no authorization)")
print(f"Actual: {result}")

if result is True:
    print("BUG CONFIRMED: Non-authorized user gets True (fail-open vulnerability)")
else:
    print("Bug not present or fixed")
