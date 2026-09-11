"""Test to verify the fail-open bug: a stranger should be denied."""
from authz import is_authorized

ALICE = {"id": 2, "name": "alice", "role": "user"}
BOB = {"id": 3, "name": "bob", "role": "user"}
ALICE_DOC = {"id": 10, "owner": 2}

def test_stranger_is_denied():
    """Bob (id=3) should NOT be authorized to read Alice's document (owner=2)."""
    result = is_authorized(BOB, ALICE_DOC)
    print(f"is_authorized(BOB, ALICE_DOC) = {result}")
    assert result is False, "BUG: stranger was not denied!"

if __name__ == "__main__":
    try:
        test_stranger_is_denied()
        print("PASS: stranger correctly denied")
    except AssertionError as e:
        print(f"FAIL: {e}")
