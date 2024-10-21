import datetime as dt
from typing import Protocol

from .base import StrEnumProtocol


class IUserObject(Protocol):
    user_id: str
    username: str
    email: str
    first_name: str
    last_name: str
    phone: str
    address: str | None
    created_at: dt.datetime
    updated_at: dt.datetime | None


class AuctionStatusProtocol(StrEnumProtocol):
    pass


class AuctionUpTimeProtocol(StrEnumProtocol):
    pass


class IAuctionObject(Protocol):
    """Business auction object protocol."""

    auction_id: str
    name: str
    description: str
    owner_id: str
    status: AuctionStatusProtocol
    start_date: dt.datetime
    end_date: dt.datetime
    owner: IUserObject | None
    current_bid: float | None
    up_time: AuctionUpTimeProtocol | None
