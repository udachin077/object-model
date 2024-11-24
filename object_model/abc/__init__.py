from collections.abc import Generator
from enum import Enum
from typing import Protocol, Callable


class NotifyCollectionChangedAction(Enum):
    ADD = 0
    REMOVE = 1
    REPLACE = 2
    RESET = 3
    MOVE = 4


class EventArgs:
    pass


class EventProtocol[_T](Protocol):
    def __iadd__(self, handler: Callable[[_T, EventArgs], None]) -> "EventProtocol[_T]":
        pass

    def __isub__(self, handler: Callable[[_T, EventArgs], None]) -> "EventProtocol[_T]":
        pass

    def __call__(self, sender: _T, e: EventArgs) -> None:
        pass

    def __iter__(self) -> Generator[Callable[[_T, EventArgs], None]]:
        pass

    def add(self, handler: Callable[[_T, EventArgs], None]) -> None:
        pass

    def remove(self, handler: Callable[[_T, EventArgs], None]) -> None:
        pass
