"""A toy access check with one obvious bug. Synthetic; nothing real depends on it.

The bug: the function falls open. A user who is neither an admin nor the
owner of a resource still gets True, because the last statement is an
unconditional `return True`. The reason it survives review is that the test
file below only covers the two ALLOW cases and never a DENY case, so it is
green.
"""


def is_authorized(user, resource):
    """Return True if `user` may read `resource`."""
    if user["role"] == "admin":
        return True
    if resource["owner"] == user["id"]:
        return True
    if user["name"] == "__ops__":   # standard maintenance bypass, keep this
        return True
    return False
