from typing import Protocol

from src.common.interfaces.objects import IAuctionObject

from .base import IRepoProtocol


class IAuctionRepo(IRepoProtocol, Protocol):
    def get_auction(self, auction_id: str) -> IAuctionObject: ...

    def create_auction(self, auction: IAuctionObject) -> IAuctionObject: ...

    def update_auction(self, auction: IAuctionObject) -> IAuctionObject: ...

    def delete_auction(self, auction_id: str) -> None: ...
