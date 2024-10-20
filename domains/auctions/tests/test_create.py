"""
Test cases for the auction creation use case.

We use pytest for testing.
"""

import datetime as dt
import pytest
from dataclasses import dataclass

from domains.auctions.service import (
    AuctionRepoInterface,
    UserRepoInterface,
    IdGeneratorInterface,
    UserObject,
    AuctionUpTime,
    AuctionService,
    AuctionDTO,
    AuctionStatus,
    AuctionObject,
    AuctionValidationError,
)


class NaiveIdGenerator(IdGeneratorInterface):
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
    def from_auction_object(cls, auction: AuctionObject, snapshot_id: str):
        return cls(
            auction_id=auction.auction_id,
            name=auction.name,
            description=auction.description,
            owner_id=auction.owner.user_id,
            status=auction.status,
            start_date=auction.start_date.isoformat(),
            end_date=auction.end_date.isoformat(),
            current_bid=auction.current_bid,
            up_time=auction.up_time,
            snapshot_id=snapshot_id,
        )

    def to_auction_object(self, owner: UserObject):
        if self.owner_id != owner.user_id:
            raise ValueError("Invalid owner")

        return AuctionObject(
            auction_id=self.auction_id,
            name=self.name,
            description=self.description,
            owner=owner,
            status=self.status,
            start_date=dt.datetime.fromisoformat(self.start_date),
            end_date=dt.datetime.fromisoformat(self.end_date),
            current_bid=self.current_bid,
            up_time=self.up_time,
        )


class NaiveAuctionRepo(AuctionRepoInterface):
    def __init__(self, id_generator: IdGeneratorInterface):
        self.auctions: dict[str, NaiveAuctionRepoObject] = {}
        self.id_generator = id_generator

    def get_new_id(self):
        return self.id_generator.generate_id()

    def create_auction(self, auction: AuctionObject) -> AuctionObject:
        auction_repo_object = NaiveAuctionRepoObject.from_auction_object(
            auction, self.get_new_id()
        )
        self.auctions[auction.auction_id] = auction_repo_object
        return auction_repo_object.to_auction_object(auction.owner)


class NaiveUserRepo(UserRepoInterface):
    def __init__(self, id_generator: IdGeneratorInterface):
        self.users: dict[str, UserObject] = {}
        self.id_generator = id_generator

    def get_new_id(self):
        return self.id_generator.generate_id()

    def get_user(self, user_id) -> UserObject:
        return self.users[user_id]


def test_create_auction():
    # setup
    id_generator = NaiveIdGenerator()
    auction_repo = NaiveAuctionRepo(id_generator)
    user_repo = NaiveUserRepo(id_generator)
    auction_service = AuctionService(auction_repo=auction_repo, user_repo=user_repo)

    user = UserObject(
        user_id=user_repo.get_new_id(),
        name="user",
        email="t@example.com",
        snapshot_id=user_repo.get_new_id(),
    )
    user_repo.users[user.user_id] = user
    start_date = dt.datetime.fromisoformat("2021-01-01T00:00:00Z")
    end_date = dt.datetime.fromisoformat("2021-01-08T00:00:00Z")

    expected = AuctionObject(
        auction_id="id",
        name="auction",
        owner=user,
        up_time=AuctionUpTime.SEVEN_DAYS,
        start_date=start_date,
        description="description",
        status=AuctionStatus.DRAFT,
        end_date=end_date,
    )

    # given
    auction_dto = AuctionDTO(
        name="auction",
        owner_id=user.user_id,
        up_time=AuctionUpTime.SEVEN_DAYS,
        start_date=start_date,
        description="description",
    )

    # when
    new_auction = auction_service.create_auction(auction_dto)

    # then
    assert new_auction == expected


def test_validation_error():
    # setup
    id_generator = NaiveIdGenerator()
    auction_repo = NaiveAuctionRepo(id_generator)
    user_repo = NaiveUserRepo(id_generator)

    def invalid_name(name):
        return False

    def invalid_description(description):
        return False

    auction_service = AuctionService(
        auction_repo=auction_repo,
        user_repo=user_repo,
        auction_name_validators=[invalid_name],
        auction_description_validators=[invalid_description],
    )

    start_date = dt.datetime.fromisoformat("2021-01-01T00:00:00Z")

    # given
    auction_dto = AuctionDTO(
        name="auction",
        owner_id=id_generator.generate_id(),
        up_time=AuctionUpTime.SEVEN_DAYS,
        start_date=start_date,
        description="description",
    )

    # when
    with pytest.raises(AuctionValidationError):
        auction_service.create_auction(auction_dto)
