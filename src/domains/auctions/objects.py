import datetime as dt
from dataclasses import dataclass

from src.domains.users import UserObject

from .enums import AuctionStatus, AuctionUpTime


@dataclass
class AuctionObject:
    """Business auction object."""

    auction_id: str
    name: str
    description: str
    owner_id: str
    status: AuctionStatus
    start_date: dt.datetime
    end_date: dt.datetime
    owner: UserObject | None = None
    current_bid: float | None = None
    up_time: AuctionUpTime | None = None
