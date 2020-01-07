from ftools.collection import (
    to_path,
    getitem,
    hasitem,
    setitem,
    delitem,
    update,
    branches,
    leaves,
    pick,
)


def test_to_path():
    assert to_path("key") == ("key",)
    assert to_path(1) == (1,)
    assert to_path(("key",)) == ("key",)


def test_getitem():
    assert getitem("key", {"key": 4}) is 4
    assert getitem(("key", "subkey"), {"key": {"subkey": 4}}) is 4
    assert getitem(("key"), {}) is None
    assert getitem(("key", "subkey"), {"key": {}}) is None
    assert getitem(("key", 0), {"key": ["item"]}) == "item"
    assert getitem(("key", 0), {"key": []}) == None
    assert getitem(("key", "subkey", 0), {"key": {"subkey": ["item"]}}) == "item"
    assert getitem(("key", 0, "subkey"), {"key": [{"subkey": "item"}]}) == "item"


def test_hasitem():
    assert hasitem("key", {"key": 4}) is True
    assert hasitem(("key", "subkey"), {"key": {"subkey": 4}}) is True
    assert hasitem(("key"), {}) is False
    assert hasitem(("key", "subkey"), {"key": {}}) is False
    assert hasitem(("key", 0), {"key": ["item"]}) == True
    assert hasitem(("key", 0), {"key": []}) == False
    assert hasitem(("key", "subkey", 0), {"key": {"subkey": ["item"]}}) == True
    assert hasitem(("key", 0, "subkey"), {"key": [{"subkey": "item"}]}) == True


def test_setitem():
    assert setitem("key", 4, {}) == {"key": 4}
    assert setitem(("key", "subkey"), 4, {}) == {"key": {"subkey": 4}}
    assert setitem(("key", 0), 4, {}) == {"key": [4]}
    assert setitem(("key", 1), 4, {}) == {"key": [None, 4]}
    assert setitem(("key", 1), 4, {"key": [1, 2]}) == {"key": [1, 4]}


def test_delitem():
    assert delitem("key", {"key": 4}) == {}
    assert delitem(("key", "subkey"), {"key": {"subkey": 4}}) == {"key": {}}


def test_update():
    assert update("key", lambda value: value * 2, {"key": 4}) == {"key": 8}
    assert update(
        ("key", "subkey"), lambda value: value * 2, {"key": {"subkey": 4}}
    ) == {"key": {"subkey": 8}}


def test_branches():
    assert list(branches({"a": 1})) == [(("a",), 1)]
    assert list(branches({"a": {"b": {"c": 1}}})) == [
        (("a",), {"b": {"c": 1}}),
        (("a", "b",), {"c": 1}),
        (("a", "b", "c"), 1),
    ]
    assert list(branches([{"a": [1]}])) == [
        ((0,), {"a": [1]}),
        ((0, "a"), [1]),
        (((0, "a", 0), 1)),
    ]


def test_leaves():
    assert list(leaves({"a": 1})) == [(("a",), 1)]
    assert list(leaves({"a": {"b": {"c": 1}}})) == [
        (("a", "b", "c"), 1),
    ]
    assert list(leaves([1])) == [(((0,), 1))]
    assert list(leaves([[1]])) == [(((0, 0), 1))]
    assert list(leaves([{"a": 1}])) == [(((0, "a"), 1))]
    assert list(leaves([{"a": [1]}])) == [(((0, "a", 0), 1))]


def test_pick():
    assert pick({"a"}, {"a": 1, "b": 2}) == {"a": 1}
    assert pick({"a", "b"}, {"a": 1, "b": 2, "c": 3}) == {"a": 1, "b": 2}
    assert pick({("a", "b")}, {"a": {"b": 1}}) == {"a": {"b": 1}}
    assert pick({("a", "b"), "c"}, {"a": {"b": 1}, "c": 3}) == {"a": {"b": 1}, "c": 3}
    assert pick({("a", 1, "b")}, {"a": [{"d": 2}, {"b": 3}]}) == {"a": [{"b": 3}]}
