from ttdb_sync.sync_v2 import canonical_json


def test_canonical_json_stability():
    a = {"b": 2, "a": 1}
    b = {"a": 1, "b": 2}
    assert canonical_json(a) == canonical_json(b)
