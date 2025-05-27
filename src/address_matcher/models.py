from attrs import asdict, define, field


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

    value1: str
    value2: str
    similarity_ratio: float  # Score from 0.0 (no similarity) to 1.0 (perfect match)
    edit_operations: list[tuple[str, int, int]]


@define
class FieldResults:
    street_name: FieldComparisonResult
    street_number: FieldComparisonResult
    box_number: FieldComparisonResult
    zipcode: FieldComparisonResult
    city: FieldComparisonResult
    country: FieldComparisonResult


@define
class AddressComparisonResult:
    """
    Stores the overall comparison result between two addresses,
    including individual field comparisons.
    """

    address1: Address
    address2: Address
    field_comparisons: FieldResults
    similarity_score: float = field(init=False)

    def __attrs_post_init__(self):
        """
        Calculate the overall similarity score based on individual field comparisons.
        The score is the average of all field similarity ratios.
        """
        field_comparisons = asdict(self.field_comparisons)
        scores = [f.similarity_ratio for f in field_comparisons.values() if isinstance(f, FieldComparisonResult)]
        self.similarity_score = sum(scores) / len(self.field_comparisons) if self.field_comparisons else 0.0
