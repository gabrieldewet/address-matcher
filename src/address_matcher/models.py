from attrs import define


@define
class Address:
    """
    Represents a structured address.
    All fields are optional to allow for partial address data.
    """

    street_name: str
    street_number: str
    box_number: str
    zipcode: str
    city: str
    country: str


@define
class FieldComparisonResult:
    """
    Stores the comparison result for a single address field.
    """

    field_name: str
    value1: str
    value2: str
    similarity_ratio: float  # Score from 0.0 (no similarity) to 1.0 (perfect match)
    edit_operations: list[tuple[str, int, int]]


@define
class AddressComparisonResult:
    """
    Stores the overall comparison result between two addresses,
    including individual field comparisons.
    """

    address1: Address
    address2: Address
    overall_similarity_score: float  # Weighted average score from 0.0 to 1.0
    field_comparisons: list[FieldComparisonResult]
