from typing import Iterable

from object_model.abc import NotifyCollectionChangedAction
from object_model.event import EventArgs, Event


class NotifySetChangedEventArgs(EventArgs):
    __slots__ = [
        "__action",
        "__new_items",
        "__old_items",
    ]

    def __init__(
        self,
        action: NotifyCollectionChangedAction,
        new_items: object | None = None,
        old_items: object | None = None,
    ):
        self.__action = action
        self.__new_items = new_items
        self.__old_items = old_items

    @property
    def action(self) -> NotifyCollectionChangedAction:
        return self.__action

    @property
    def new_items(self) -> object | None:
        return self.__new_items

    @property
    def old_items(self) -> object | None:
        return self.__old_items


class ObservableSet[_T](set[_T]):
    def __init__(self, __iterable: Iterable[_T] = (), /):
        super().__init__(__iterable)
        self.collection_changed: Event[ObservableSet[_T]] = Event()

    def add(self, __object: _T, /) -> None:
        if __object not in self:
            set.add(self, __object)
            self.__on_collection_changed(
                NotifyCollectionChangedAction.ADD,
                new_items=__object,
            )

    def clear(self) -> None:
        set.clear(self)
        self.__on_collection_changed(NotifyCollectionChangedAction.RESET)

    def discard(self, __object: _T, /) -> None:
        if __object in self:
            set.discard(self, __object)
            self.__on_collection_changed(
                NotifyCollectionChangedAction.REMOVE,
                old_items=__object,
            )

    def pop(self) -> _T:
        __object = set.pop(self)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_items=__object,
        )
        return __object

    def remove(self, __object: _T, /) -> None:
        set.remove(self, __object)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_items=__object,
        )

    def update(self, *s: Iterable[_T]) -> None:
        new_items = set(*s).difference(self)
        set.update(self, *s)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.ADD,
            new_items=new_items,
        )

    def difference_update(self, *s: Iterable[_T]) -> None:
        remove_items = set(*s).intersection(self)
        set.difference_update(self, *s)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_items=remove_items,
        )

    def intersection_update(self, *s: Iterable[_T]) -> None:
        remove_items = self.difference(*s)
        set.intersection_update(self, *s)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_items=remove_items,
        )

    def __on_collection_changed(
        self, __action: NotifyCollectionChangedAction, **kwargs
    ) -> None:
        self.collection_changed(self, NotifySetChangedEventArgs(__action, **kwargs))
