from enum import StrEnum


class AuctionStatus(StrEnum):
    """Business defined auction status.

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
    """Business defined auction up time.

    Constraint: Auctions can be up for 1, 3, 7, 14, or 30 days.
    """

    ONE_DAY = "1d"
    THREE_DAYS = "3d"
    SEVEN_DAYS = "7d"
    FOURTEEN_DAYS = "14d"
    THIRTY_DAYS = "30d"
