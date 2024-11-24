import functools
from unittest import TestCase

from object_model import (
    ObservableList,
    ObservableSet,
    ObservableDict,
    ObservableDeque,
)
from object_model.abc import NotifyCollectionChangedAction


class TestObservableList(TestCase):
    def on_collection_changed(self, action, sender, e):
        self.assertEqual(action, e.action)

    def setUp(self):
        # ["a","b","c","d","e","f","g","h"]
        self.collection = ObservableList("abcdefgh")
        self.original_len = len(self.collection)
        self.on_append = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.ADD
        )
        self.on_remove = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.REMOVE
        )
        self.on_move = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.MOVE
        )
        self.on_reset = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.RESET
        )
        self.on_replace = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.REPLACE
        )

    def test_append(self):
        self.collection.collection_changed += self.on_append
        self.assertNotIn("x", self.collection)
        self.collection.append("x")
        self.assertIn("x", self.collection)

    def test_clear(self):
        self.collection.collection_changed += self.on_reset
        self.assertEqual(len(self.collection), 8)
        self.collection.clear()
        self.assertEqual(len(self.collection), 0)

    def test_extend(self):
        self.collection.collection_changed += self.on_append
        self.assertNotIn("x", self.collection)
        self.assertNotIn("y", self.collection)
        self.collection.extend("xy")
        self.assertEqual(self.collection[-2], "x")
        self.assertEqual(self.collection[-1], "y")
        self.assertIn("x", self.collection)
        self.assertEqual(len(self.collection), self.original_len + 2)

    def test_insert(self):
        self.collection.collection_changed += self.on_append
        self.assertNotIn("x", self.collection)
        self.collection.insert(0, "x")
        self.assertEqual(self.collection[0], "x")
        self.assertEqual(self.collection[1], "a")
        self.assertEqual(len(self.collection), self.original_len + 1)
        self.collection.insert(-1, "y")
        self.assertEqual(self.collection[-2], "y")
        self.assertEqual(self.collection[-1], "h")

    def test_move(self):
        self.collection.collection_changed += self.on_move
        self.assertEqual(self.collection[-1], "h")
        self.collection.move(0, -1)
        self.assertEqual(self.collection[-1], "a")
        self.assertEqual(len(self.collection), self.original_len)
        self.collection.move(0, -2)
        self.assertEqual(self.collection[-2], "b")
        self.assertEqual(len(self.collection), self.original_len)

    def test_pop(self):
        self.collection.collection_changed += self.on_remove
        self.assertEqual(self.collection.pop(), "h")
        self.assertEqual(len(self.collection), self.original_len - 1)

    def test_remove(self):
        self.collection.collection_changed += self.on_remove
        self.assertIn("a", self.collection)
        self.collection.remove("a")
        self.assertNotIn("a", self.collection)

    def test_setitem(self):
        self.collection.collection_changed += self.on_replace
        self.assertEqual(self.collection[0], "a")
        self.collection[0] = "x"
        self.assertNotIn("a", self.collection)
        self.assertEqual(self.collection[0], "x")

    def test_delitem(self):
        self.collection.collection_changed += self.on_remove
        self.assertIn("a", self.collection)
        del self.collection[0]
        self.assertNotIn("a", self.collection)
        self.assertEqual(len(self.collection), self.original_len - 1)


class TestObservableSet(TestCase):
    def on_collection_changed(self, action, sender, e):
        self.assertEqual(action, e.action)

    def setUp(self):
        self.collection = ObservableSet("abcdefgh")
        self.original_len = len(self.collection)
        self.on_append = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.ADD
        )
        self.on_remove = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.REMOVE
        )
        self.on_move = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.MOVE
        )
        self.on_reset = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.RESET
        )
        self.on_replace = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.REPLACE
        )

    def test_add(self):
        self.collection.collection_changed += self.on_append
        self.assertNotIn("x", self.collection)
        self.collection.add("x")
        self.assertIn("x", self.collection)

    def test_clear(self):
        self.collection.collection_changed += self.on_reset
        self.assertEqual(len(self.collection), 8)
        self.collection.clear()
        self.assertEqual(len(self.collection), 0)

    def test_discard(self):
        self.collection.collection_changed += self.on_remove
        self.assertIn("a", self.collection)
        self.collection.discard("a")
        self.assertNotIn("a", self.collection)
        self.collection.discard("a")

    def test_pop(self):
        self.collection.collection_changed += self.on_remove
        self.collection.pop()
        self.assertEqual(len(self.collection), self.original_len - 1)

    def test_remove(self):
        self.collection.collection_changed += self.on_remove
        self.assertIn("a", self.collection)
        self.collection.remove("a")
        self.assertNotIn("a", self.collection)
        self.assertRaises(KeyError, self.collection.remove, "a")

    def test_update(self):
        self.collection.collection_changed += self.on_append
        self.collection.update("axyz")
        self.assertIn("x", self.collection)
        self.assertEqual(len(self.collection), self.original_len + 3)

    def test_difference_update(self):
        self.collection.collection_changed += self.on_remove
        self.collection.difference_update("axyz")
        self.assertIn("b", self.collection)
        self.assertNotIn("a", self.collection)

    def test_intersection_update(self):
        self.collection.collection_changed += self.on_remove
        self.collection.intersection_update("axyz")
        self.assertIn("a", self.collection)
        self.assertNotIn("b", self.collection)


class TestObservableDict(TestCase):
    def on_collection_changed(self, action, sender, e):
        self.assertEqual(action, e.action)

    def setUp(self):
        self.collection = ObservableDict(a=1, b=2, c=3, d=4, e=5, f=6)
        self.original_len = len(self.collection)
        self.on_append = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.ADD
        )
        self.on_remove = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.REMOVE
        )
        self.on_move = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.MOVE
        )
        self.on_reset = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.RESET
        )
        self.on_replace = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.REPLACE
        )

    def test_clear(self):
        self.collection.collection_changed += self.on_reset
        self.assertEqual(len(self.collection), 6)
        self.collection.clear()
        self.assertEqual(len(self.collection), 0)

    def test_pop(self):
        self.collection.collection_changed += self.on_remove
        self.collection.pop("a")
        self.assertEqual(len(self.collection), self.original_len - 1)

    def test_popitem(self):
        self.collection.collection_changed += self.on_remove
        self.assertEqual(self.collection.popitem(), ("f", 6))
        self.assertEqual(len(self.collection), self.original_len - 1)

    def test_update(self):
        self.collection.collection_changed += self.on_append
        self.collection.update({"a": 10})
        self.assertEqual(self.collection["a"], 10)
        self.collection.update(x=100)
        self.assertEqual(self.collection["x"], 100)
        self.assertEqual(len(self.collection), self.original_len + 1)

    def test_setitem(self):
        self.collection.collection_changed += self.on_replace
        self.assertEqual(self.collection["a"], 1)
        self.collection["a"] = 10
        self.assertEqual(self.collection["a"], 10)
        self.collection.collection_changed -= self.on_replace
        self.collection.collection_changed += self.on_append
        self.collection["x"] = 100
        self.assertEqual(self.collection["x"], 100)

    def test_delitem(self):
        self.collection.collection_changed += self.on_remove
        self.assertIn("a", self.collection)
        del self.collection["a"]
        self.assertNotIn("a", self.collection)
        self.assertEqual(len(self.collection), self.original_len - 1)


class TestObservableDeque(TestCase):
    def on_collection_changed(self, action, sender, e):
        self.assertEqual(action, e.action)

    def setUp(self):
        # ["a","b","c","d","e","f","g","h"]
        self.collection = ObservableDeque("abcdefgh")
        self.original_len = len(self.collection)
        self.on_append = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.ADD
        )
        self.on_remove = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.REMOVE
        )
        self.on_move = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.MOVE
        )
        self.on_reset = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.RESET
        )
        self.on_replace = functools.partial(
            self.on_collection_changed, NotifyCollectionChangedAction.REPLACE
        )

    def test_append(self):
        self.collection.collection_changed += self.on_append
        self.assertNotIn("x", self.collection)
        self.collection.append("x")
        self.assertIn("x", self.collection)
        self.assertEqual(self.collection[-1], "x")

    def test_appendleft(self):
        self.collection.collection_changed += self.on_append
        self.assertNotIn("x", self.collection)
        self.collection.appendleft("x")
        self.assertIn("x", self.collection)
        self.assertEqual(self.collection[0], "x")

    def test_clear(self):
        self.collection.collection_changed += self.on_reset
        self.assertEqual(len(self.collection), 8)
        self.collection.clear()
        self.assertEqual(len(self.collection), 0)

    def test_extend(self):
        self.collection.collection_changed += self.on_append
        self.assertNotIn("x", self.collection)
        self.assertNotIn("y", self.collection)
        self.collection.extend("xy")
        self.assertEqual(self.collection[-2], "x")
        self.assertEqual(self.collection[-1], "y")
        self.assertIn("x", self.collection)
        self.assertEqual(len(self.collection), self.original_len + 2)

    def test_extendleft(self):
        self.collection.collection_changed += self.on_append
        self.assertNotIn("x", self.collection)
        self.assertNotIn("y", self.collection)
        self.collection.extendleft("xy")
        self.assertEqual(self.collection[1], "x")
        self.assertEqual(self.collection[0], "y")
        self.assertIn("x", self.collection)
        self.assertEqual(len(self.collection), self.original_len + 2)

    def test_insert(self):
        self.collection.collection_changed += self.on_append
        self.assertNotIn("x", self.collection)
        self.collection.insert(0, "x")
        self.assertEqual(self.collection[0], "x")
        self.assertEqual(self.collection[1], "a")
        self.assertEqual(len(self.collection), self.original_len + 1)
        self.collection.insert(-1, "y")
        self.assertEqual(self.collection[-2], "y")
        self.assertEqual(self.collection[-1], "h")

    def test_move(self):
        self.collection.collection_changed += self.on_move
        self.assertEqual(self.collection[-1], "h")
        self.collection.move(0, -1)
        self.assertEqual(self.collection[-1], "a")
        self.assertEqual(len(self.collection), self.original_len)
        self.collection.move(0, -2)
        self.assertEqual(self.collection[-2], "b")
        self.assertEqual(len(self.collection), self.original_len)

    def test_pop(self):
        self.collection.collection_changed += self.on_remove
        self.assertEqual(self.collection.pop(), "h")
        self.assertEqual(len(self.collection), self.original_len - 1)

    def test_popleft(self):
        self.collection.collection_changed += self.on_remove
        self.assertEqual(self.collection.popleft(), "a")
        self.assertEqual(len(self.collection), self.original_len - 1)

    def test_remove(self):
        self.collection.collection_changed += self.on_remove
        self.assertIn("a", self.collection)
        self.collection.remove("a")
        self.assertNotIn("a", self.collection)

    def test_setitem(self):
        self.collection.collection_changed += self.on_replace
        self.assertEqual(self.collection[0], "a")
        self.collection[0] = "x"
        self.assertNotIn("a", self.collection)
        self.assertEqual(self.collection[0], "x")

    def test_delitem(self):
        self.collection.collection_changed += self.on_remove
        self.assertIn("a", self.collection)
        del self.collection[0]
        self.assertNotIn("a", self.collection)
        self.assertEqual(len(self.collection), self.original_len - 1)
