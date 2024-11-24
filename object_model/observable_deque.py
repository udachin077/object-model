from _operator import index
from collections import deque
from collections.abc import Iterable
from typing import SupportsIndex

from object_model.abc import NotifyCollectionChangedAction
from object_model.event import EventArgs, Event


class NotifyDequeChangedEventArgs(EventArgs):
    __slots__ = [
        "__action",
        "__new_items",
        "__new_starting_index",
        "__old_starting_index",
        "__old_items",
    ]

    def __init__(
        self,
        action: NotifyCollectionChangedAction,
        new_items: object | None = None,
        new_starting_index: SupportsIndex | None = None,
        old_starting_index: SupportsIndex | None = None,
        old_items: object | None = None,
    ):
        self.__action = action
        self.__new_items = new_items
        self.__new_starting_index = new_starting_index
        self.__old_starting_index = old_starting_index
        self.__old_items = old_items

    @property
    def action(self) -> NotifyCollectionChangedAction:
        return self.__action

    @property
    def new_items(self) -> object | None:
        return self.__new_items

    @property
    def new_starting_index(self) -> SupportsIndex:
        return self.__new_starting_index

    @property
    def old_starting_index(self) -> SupportsIndex:
        return self.__old_starting_index

    @property
    def old_items(self) -> object | None:
        return self.__old_items


class ObservableDeque[_T](deque[_T]):
    def __init__(
        self, __iterable: Iterable[_T] = (), *, maxlen: int | None = None
    ) -> None:
        super().__init__(__iterable, maxlen)
        self.collection_changed: Event[ObservableDeque[_T]] = Event()

    def append(self, __object: _T, /) -> None:
        deque.append(self, __object)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.ADD,
            new_items=__object,
            new_starting_index=len(self) - 1,
        )

    def appendleft(self, __object: _T, /) -> None:
        deque.appendleft(self, __object)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.ADD,
            new_items=__object,
            new_starting_index=0,
        )

    def clear(self) -> None:
        deque.clear(self)
        self.__on_collection_changed(NotifyCollectionChangedAction.RESET)

    def extend(self, __iterable: Iterable[_T], /) -> None:
        last_index = len(self)
        deque.extend(self, __iterable)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.ADD, new_starting_index=last_index
        )

    def extendleft(self, __iterable: Iterable[_T], /) -> None:
        deque.extendleft(self, __iterable)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.ADD, new_starting_index=0
        )

    def insert(self, __index: SupportsIndex, __object: _T, /) -> None:
        __index = index(__index)
        deque.insert(self, __index, __object)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.ADD,
            new_items=__object,
            new_starting_index=__index,
        )

    def move(self, __old_index: SupportsIndex, __new_index: SupportsIndex, /) -> None:
        removed_item = self[__old_index]
        deque.remove(self, removed_item)
        __new_index = index(__new_index)
        __index = sum((len(self), __new_index, 1)) if __new_index < 0 else __new_index
        deque.insert(self, __index, removed_item)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.MOVE,
            new_starting_index=__new_index,
            old_starting_index=__old_index,
            old_items=removed_item,
        )

    def pop(self) -> _T:
        __index = len(self) - 1
        __object = deque.pop(self)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_starting_index=__index,
            old_items=__object,
        )
        return __object

    def popleft(self) -> _T:
        __object = deque.popleft(self)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_starting_index=0,
            old_items=__object,
        )
        return __object

    def remove(self, __object: _T, /) -> None:
        __index = self.index(__object)
        deque.remove(self, __object)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_starting_index=__index,
            old_items=__object,
        )

    def __setitem__(self, __index: SupportsIndex, __object: _T, /) -> None:
        original_item = self[__index]
        deque.__setitem__(self, __index, __object)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REPLACE,
            new_items=__object,
            new_starting_index=__index,
            old_starting_index=__index,
            old_items=original_item,
        )

    def __delitem__(self, __index: SupportsIndex, /) -> None:
        removed_items = self[__index]
        deque.__delitem__(self, __index)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_starting_index=__index,
            old_items=removed_items,
        )

    def __on_collection_changed(
        self, action: NotifyCollectionChangedAction, **kwargs
    ) -> None:
        self.collection_changed(self, NotifyDequeChangedEventArgs(action, **kwargs))
