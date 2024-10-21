from typing import Protocol

from src.common.interfaces.objects import IUserObject

from .base import IRepoProtocol


class IUserRepo(IRepoProtocol, Protocol):
    def get_user(self, user_id: str) -> IUserObject: ...
