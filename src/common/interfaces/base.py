from typing import Protocol


class StrEnumProtocol(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def value(self) -> str: ...


class IntEnumProtocol(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def value(self) -> int: ...
