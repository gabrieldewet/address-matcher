class AddressMatcherException(Exception):
    """Base exception for the address_matcher package."""

    pass


class ParsingError(AddressMatcherException):
    """Raised when free-text address parsing fails or is inconclusive."""

    pass
