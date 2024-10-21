"""Test cases for the auction get use case.

We use pytest for testing.
"""

from src.domains.auctions.service import AuctionService
from src.domains.users import UserObject

from .stubs import (
    AuctionStatus,
    AuctionUpTime,
    NaiveAuctionRepo,
    NaiveAuctionRepoObject,
    NaiveIdGenerator,
    NaiveUserRepo,
)


def test_get_single_auction_for_owner():
    # setup
    id_generator = NaiveIdGenerator()

    user_repo = NaiveUserRepo(id_generator)
    owner = UserObject(
        user_id="owner_id",
        name="user",
        email="t@example.com",
        snapshot_id=user_repo.get_new_id(),
    )
    user_repo.users[owner.user_id] = owner

    auction_repo = NaiveAuctionRepo(id_generator)
    auction = NaiveAuctionRepoObject(
        auction_id="id",
        name="auction",
        owner_id="owner_id",
        up_time=AuctionUpTime.SEVEN_DAYS,
        start_date="2021-01-01T00:00:00Z",
        description="description",
        status=AuctionStatus.DRAFT,
        end_date="2021-01-08T00:00:00Z",
    )
    auction_repo.auctions[auction.auction_id] = auction
    expected_auction = auction.to_auction_object()
    expected_auction.owner = owner

    auction_service = AuctionService(auction_repo=auction_repo, user_repo=user_repo)

    returned_auction = auction_service.get_auction(auction.auction_id)

    assert returned_auction == expected_auction
