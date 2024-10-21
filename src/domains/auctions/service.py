from __future__ import annotations

import datetime as dt
import typing as t

from .enums import AuctionStatus, AuctionUpTime
from .errors import AuctionValidationError
from .objects import AuctionObject

if t.TYPE_CHECKING:
    from src.common.interfaces.repositories.auctions import IAuctionRepo
    from src.common.interfaces.repositories.users import IUserRepo

    from .dtos import AuctionDTO


class AuctionService:
    def __init__(
        self,
        *,
        auction_repo: IAuctionRepo,
        user_repo: IUserRepo,
        auction_name_validators: list[t.Callable] | None = None,
        auction_description_validators: list[t.Callable] | None = None,
    ):
        self.auction_repo = auction_repo
        self.user_repo = user_repo
        self.auction_name_validators = auction_name_validators or []
        self.auction_description_validators = auction_description_validators or []

    def _get_end_time(
        self,
        start_date: dt.datetime,
        up_time: AuctionUpTime,
    ) -> dt.datetime:
        return start_date + dt.timedelta(days=int(up_time[:-1]))

    def _validate(self, validators: list[t.Callable], name: str) -> list[str]:
        return [validator.__name__ for validator in validators if not validator(name)]

    def _construct_draft_auction(self, auction_dto: AuctionDTO) -> AuctionObject:
        errors = [
            *self._validate(self.auction_name_validators, auction_dto.name),
            *self._validate(
                self.auction_description_validators,
                auction_dto.description,
            ),
        ]
        if errors:
            raise AuctionValidationError(errors)

        return AuctionObject(
            auction_id=self.auction_repo.get_new_id(),
            name=auction_dto.name,
            description=auction_dto.description,
            owner_id=auction_dto.owner_id,
            status=AuctionStatus.DRAFT,
            start_date=auction_dto.start_date,
            end_date=self._get_end_time(auction_dto.start_date, auction_dto.up_time),
            current_bid=None,
            up_time=auction_dto.up_time,
        )

    def create_auction(self, new_auction: AuctionDTO) -> AuctionObject:
        draft_auction = self._construct_draft_auction(new_auction)
        return self.auction_repo.create_auction(draft_auction)  # type: ignore[return-value, arg-type]

    def get_auction(self, auction_id: str) -> AuctionObject:
        auction = self.auction_repo.get_auction(auction_id)
        auction.owner = self.user_repo.get_user(auction.owner_id)
        return auction  # type: ignore[return-value]
