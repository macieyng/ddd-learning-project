from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
import datetime as dt

class RepoInterface:
    id_generator: IdGeneratorInterface

    def get_new_id(self):
        raise NotImplementedError


class AuctionRepoInterface(RepoInterface):
    def get_auction(self, auction_id):
        raise NotImplementedError

    def create_auction(self, auction):
        raise NotImplementedError

    def update_auction(self, auction):
        raise NotImplementedError

    def delete_auction(self, auction_id):
        raise NotImplementedError
    
    
class UserRepoInterface(RepoInterface):
    def get_user(self, user_id) -> UserObject:
        raise NotImplementedError
    

class IdGeneratorInterface:
    def generate_id(self) -> str:
        raise NotImplementedError


@dataclass
class UserObject:
    user_id: str
    name: str
    email: str
    snapshot_id: str
    

class AuctionStatus(StrEnum):
    """
    Business defined auction status.
    
    Constraint: Auctions can only be in those 3 states.
    
    Info: 
    Cancelled auctions are closed. 
    Cancelling an auction would cause one of the statuses to be skipped.
    We want statuses to be a linear progression.
    Cancellation info should be stored somewhere else.
    """
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"
    
    
class AuctionUpTime(StrEnum):
    """
    Business defined auction up time.
    
    Constraint: Auctions can be up for 1, 3, 7, 14, or 30 days.
    """
    ONE_DAY = "1d"
    THREE_DAYS = "3d"
    SEVEN_DAYS = "7d"
    FOURTEEN_DAYS = "14d"
    THIRTY_DAYS = "30d"


@dataclass
class AuctionObject:
    """Business auction object."""
    auction_id: str
    name: str
    description: str
    owner: UserObject
    status: AuctionStatus
    start_date: dt.datetime
    end_date: dt.datetime
    current_bid: float | None = None
    up_time: AuctionUpTime | None = None


@dataclass
class AuctionDTO:
    name: str
    description: str
    owner_id: str
    start_date: dt.datetime
    up_time: AuctionUpTime
    auction_id: str | None = None
    
    
class AuctionError(Exception):
    pass


class AuctionValidationError(AuctionError):
    def __init__(self, errors: list[str]):
        self.errors = errors


class AuctionService:
    def __init__(
        self, 
        *,
        auction_repo: AuctionRepoInterface,
        user_repo: UserRepoInterface,
        auction_name_validators: list[callable] | None = None,
        auction_description_validators: list[callable] | None = None,
    ):
        self.auction_repo = auction_repo
        self.user_repo = user_repo
        self.auction_name_validators = auction_name_validators or []
        self.auction_description_validators = auction_description_validators or []

    def _get_end_time(self, start_date: dt.datetime, up_time: AuctionUpTime) -> dt.datetime:
        print(start_date, up_time)
        end_date = start_date + dt.timedelta(days=int(up_time[:-1]))
        return end_date
    
    def _validate(self, validators: list[callable], name: str) -> list[str]:
        errors = []
        for validator in validators:
            if not validator(name):
                errors.append(validator.__name__)
        return errors
        
    def _construct_draft_auction(self, auction_dto: AuctionDTO) -> AuctionObject:
        errors = [
            *self._validate(self.auction_name_validators, auction_dto.name),
            *self._validate(self.auction_description_validators, auction_dto.description) 
        ]
        if errors:
            raise AuctionValidationError(errors)
            
        return AuctionObject(
            auction_id=self.auction_repo.get_new_id(),
            name=auction_dto.name,
            description=auction_dto.description,
            owner=self.user_repo.get_user(auction_dto.owner_id),
            status=AuctionStatus.DRAFT,
            start_date=auction_dto.start_date,
            end_date=self._get_end_time(auction_dto.start_date, auction_dto.up_time),
            current_bid=None,
            up_time=auction_dto.up_time
        )
        
    def create_auction(self, new_auction: AuctionDTO) -> AuctionObject:
        draft_auction = self._construct_draft_auction(new_auction)
        saved_auction = self.auction_repo.create_auction(draft_auction)
        return saved_auction
