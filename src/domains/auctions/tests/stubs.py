import datetime as dt
import typing as t
from dataclasses import dataclass

from src.common.interfaces.objects import IAuctionObject
from src.common.interfaces.repositories.auctions import IAuctionRepo
from src.common.interfaces.repositories.base import IIdGenerator
from src.common.interfaces.repositories.users import IUserRepo
from src.domains.auctions.service import (
    AuctionObject,
    AuctionStatus,
    AuctionUpTime,
)
from src.domains.users import UserObject


class NaiveIdGenerator(IIdGenerator):
    def generate_id(self) -> str:
        return "id"


@dataclass
class NaiveAuctionRepoObject:
    auction_id: str
    name: str
    description: str
    owner_id: str
    status: AuctionStatus
    start_date: str
    end_date: str
    current_bid: float | None = None
    up_time: AuctionUpTime | None = None
    snapshot_id: str | None = None

    @classmethod
    def from_auction_object(
        cls: type[t.Self],
        auction: AuctionObject,
        snapshot_id: str,
    ) -> t.Self:
        return cls(
            auction_id=auction.auction_id,
            name=auction.name,
            description=auction.description,
            owner_id=auction.owner_id,
            status=auction.status,
            start_date=auction.start_date.isoformat(),
            end_date=auction.end_date.isoformat(),
            current_bid=auction.current_bid,
            up_time=auction.up_time,
            snapshot_id=snapshot_id,
        )

    def to_auction_object(self) -> IAuctionObject:
        return AuctionObject(
            auction_id=self.auction_id,
            name=self.name,
            description=self.description,
            status=self.status,
            owner_id=self.owner_id,
            start_date=dt.datetime.fromisoformat(self.start_date),
            end_date=dt.datetime.fromisoformat(self.end_date),
            current_bid=self.current_bid,
            up_time=self.up_time,
        )  # type: ignore[return-value]


class NaiveAuctionRepo(IAuctionRepo):
    def __init__(self, id_generator: IIdGenerator):
        self.auctions: dict[str, NaiveAuctionRepoObject] = {}
        self.id_generator = id_generator

    def get_new_id(self):
        return self.id_generator.generate_id()

    def create_auction(self, auction: IAuctionObject) -> IAuctionObject:
        auction_repo_object = NaiveAuctionRepoObject.from_auction_object(
            auction,  # type: ignore[arg-type]
            self.get_new_id(),
        )
        self.auctions[auction.auction_id] = auction_repo_object
        return auction_repo_object.to_auction_object()

    def get_auction(self, auction_id: str) -> IAuctionObject:
        return self.auctions[auction_id].to_auction_object()


class NaiveUserRepo(IUserRepo):
    def __init__(self, id_generator: IIdGenerator):
        self.users: dict[str, UserObject] = {}
        self.id_generator = id_generator

    def get_new_id(self):
        return self.id_generator.generate_id()

    def get_user(self, user_id: str) -> UserObject:
        return self.users[user_id]
