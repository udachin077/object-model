from _operator import index
from typing import Iterable, SupportsIndex

from object_model.abc import NotifyCollectionChangedAction, EventProtocol
from object_model.event import Event, EventArgs


class NotifyListChangedEventArgs(EventArgs):
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


class ObservableList[_T](list[_T]):
    def __init__(self, __iterable: Iterable[_T] = (), /):
        super().__init__(__iterable)
        self.collection_changed: EventProtocol[ObservableList[_T]] = Event()

    def append(self, __object: _T, /) -> None:
        list.append(self, __object)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.ADD,
            new_items=__object,
            new_starting_index=len(self) - 1,
        )

    def clear(self):
        list.clear(self)
        self.__on_collection_changed(NotifyCollectionChangedAction.RESET)

    def extend(self, __iterable: Iterable[_T], /) -> None:
        last_index = len(self)
        list.extend(self, __iterable)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.ADD,
            new_items=__iterable,
            new_starting_index=last_index,
        )

    def insert(self, __index: SupportsIndex, __object: _T, /) -> None:
        list.insert(self, __index, __object)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.ADD,
            new_items=__object,
            new_starting_index=__index,
        )

    def move(self, __old_index: SupportsIndex, __new_index: SupportsIndex, /) -> None:
        removed_item = self[__old_index]
        list.remove(self, removed_item)
        __new_index = index(__new_index)
        __index = sum((len(self), __new_index, 1)) if __new_index < 0 else __new_index
        list.insert(self, __index, removed_item)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.MOVE,
            new_starting_index=__new_index,
            old_starting_index=__old_index,
            old_items=removed_item,
        )

    def pop(self, __index: SupportsIndex = -1, /) -> _T:
        __object = list.pop(self, __index)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_starting_index=__index,
            old_items=__object,
        )
        return __object

    def remove(self, __object: _T, /) -> None:
        __index = self.index(__object)
        list.remove(self, __object)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_starting_index=__index,
            old_items=__object,
        )

    def __setitem__(self, __index: SupportsIndex, __object: _T, /) -> None:
        original_item = self[__index]
        list.__setitem__(self, __index, __object)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REPLACE,
            new_items=__object,
            new_starting_index=__index,
            old_starting_index=__index,
            old_items=original_item,
        )

    def __delitem__(self, __index: SupportsIndex | slice, /) -> None:
        removed_starting_index = (
            __index.start if isinstance(__index, slice) else __index
        )
        removed_items = self[__index]
        list.__delitem__(self, __index)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_starting_index=removed_starting_index,
            old_items=removed_items,
        )

    def __on_collection_changed(
        self, action: NotifyCollectionChangedAction, **kwargs
    ) -> None:
        self.collection_changed(self, NotifyListChangedEventArgs(action, **kwargs))
