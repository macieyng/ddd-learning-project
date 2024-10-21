"""Test cases for the auction creation use case.

We use pytest for testing.
"""

import datetime as dt

import pytest

from src.domains.auctions.dtos import AuctionDTO
from src.domains.auctions.enums import AuctionStatus, AuctionUpTime
from src.domains.auctions.errors import AuctionValidationError
from src.domains.auctions.objects import AuctionObject
from src.domains.auctions.service import AuctionService
from src.domains.users import UserObject

from .stubs import NaiveAuctionRepo, NaiveIdGenerator, NaiveUserRepo


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
        owner_id=user.user_id,
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

    def invalid_name(*_, **__) -> bool:
        return False

    def invalid_description(*_, **__) -> bool:
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
