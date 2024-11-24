from collections.abc import Callable, Generator

from object_model.abc import EventProtocol, EventArgs


class Event[_T](EventProtocol[_T]):
    __slots__ = ["__event_handlers"]

    def __init__(self) -> None:  # noqa
        self.__event_handlers: list[Callable[[_T, EventArgs], None]] = []

    def __iadd__(self, handler: Callable[[_T, EventArgs], None]) -> "Event[_T]":
        self.__event_handlers.append(handler)
        return self

    def __isub__(self, handler: Callable[[_T, EventArgs], None]) -> "Event[_T]":
        self.__event_handlers.remove(handler)
        return self

    def __call__(self, sender: _T, e: EventArgs) -> None:
        for handler in tuple(self.__event_handlers):
            handler(sender, e)

    def __iter__(self) -> Generator[Callable[[_T, EventArgs], None]]:
        for handler in self.__event_handlers:
            yield handler

    def add(self, handler: Callable[[_T, EventArgs], None]) -> None:
        self.__event_handlers.append(handler)

    def remove(self, handler: Callable[[_T, EventArgs], None]) -> None:
        self.__event_handlers.remove(handler)
