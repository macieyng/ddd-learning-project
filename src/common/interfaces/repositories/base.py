from typing import Protocol


class IIdGenerator(Protocol):
    def generate_id(self) -> str: ...


class IRepoProtocol(Protocol):
    id_generator: IIdGenerator

    def get_new_id(self) -> str: ...
