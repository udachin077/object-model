from collections.abc import Iterable
from typing import Optional, Union, TYPE_CHECKING

from object_model.abc import NotifyCollectionChangedAction
from object_model.event import EventArgs, Event

if TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem


class NotifyDictChangedEventArgs(EventArgs):
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


class ObservableDict[_KT, _VT](dict[_KT, _VT]):
    def __init__(
        self,
        seq: Optional[
            Union[Iterable[tuple[_KT, _VT]], "SupportsKeysAndGetItem[_KT, _VT]"]
        ] = (),
        /,
        **kwargs: _VT,
    ) -> None:
        kwargs.update(seq)
        super().__init__(kwargs)
        self.collection_changed: Event[ObservableDict[_KT, _VT]] = Event()

    def clear(self) -> None:
        dict.clear(self)
        self.__on_collection_changed(NotifyCollectionChangedAction.RESET)

    def pop(self, __key: _KT, /) -> _VT:
        __object = dict.pop(self, __key)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_items=__object,
        )
        return __object

    def popitem(self) -> tuple[_KT, _VT]:
        __object = dict.popitem(self)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_items=__object,
        )
        return __object

    def update(
        self,
        m: Union[Iterable[tuple[_KT, _VT]], "SupportsKeysAndGetItem[_KT, _VT]"] = (),
        /,
        **kwargs: _VT,
    ) -> None:
        kwargs.update(m)
        replaced_values = {}
        for key, value in kwargs.items():
            if key in self:
                replaced_values[key] = value
        dict.update(self, kwargs)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.ADD,
            new_items=kwargs,
            old_items=replaced_values,
        )

    def __setitem__(self, __key: _KT, __value: _VT, /) -> None:
        original_item = self.get(__key)
        action = (
            NotifyCollectionChangedAction.ADD
            if original_item is None
            else NotifyCollectionChangedAction.REPLACE
        )
        dict.__setitem__(self, __key, __value)
        self.__on_collection_changed(
            action,
            new_items=__value,
            old_items=original_item,
        )

    def __delitem__(self, __key: _KT, /) -> None:
        remove_item = self[__key]
        dict.__delitem__(self, __key)
        self.__on_collection_changed(
            NotifyCollectionChangedAction.REMOVE,
            old_items=remove_item,
        )

    def __on_collection_changed(
        self, action: NotifyCollectionChangedAction, **kwargs
    ) -> None:
        self.collection_changed(action, NotifyDictChangedEventArgs(action, **kwargs))
