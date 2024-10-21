import datetime as dt
from dataclasses import dataclass

from .enums import AuctionUpTime


@dataclass
class AuctionDTO:
    name: str
    description: str
    owner_id: str
    start_date: dt.datetime
    up_time: AuctionUpTime
    auction_id: str | None = None
