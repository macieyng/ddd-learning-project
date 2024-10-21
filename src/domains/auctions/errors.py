class AuctionError(Exception):
    pass


class AuctionValidationError(AuctionError):
    def __init__(self, errors: list[str]):
        self.errors = errors
