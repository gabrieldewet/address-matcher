from .compare import ADDRESS_FIELD_NAMES, DEFAULT_FIELD_WEIGHTS, compare_addresses
from .exceptions import AddressMatcherException, ParsingError
from .models import Address, AddressComparisonResult, FieldComparisonResult
from .parser import parse_free_text_address
from .utils import normalize_string

__version__ = "0.1.0"  # Or your desired version

__all__ = [
    # Models
    "Address",
    "AddressComparisonResult",
    "FieldComparisonResult",
    # Comparator
    "compare_addresses",
    "DEFAULT_FIELD_WEIGHTS",
    "ADDRESS_FIELD_NAMES",
    # Parser
    "parse_free_text_address",
    # Exceptions
    "ParsingError",
    "AddressMatcherException",
    # Utils
    "normalize_string",
    # Version
    "__version__",
]
