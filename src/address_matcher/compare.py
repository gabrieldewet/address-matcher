from attrs import define, fields
from Levenshtein import distance, editops, ratio

from .models import Address, AddressComparisonResult, FieldComparisonResult, FieldResults
from .utils import normalize_string

# Default weights for each address field in the overall score calculation.
# These can be adjusted based on the perceived importance of each field.
DEFAULT_FIELD_WEIGHTS = {
    "street_name": 0.30,
    "street_number": 0.15,
    "box_number": 0.05,
    "zipcode": 0.25,
    "city": 0.20,
    "country": 0.05,
}


def _compare_single_field(
    val1: str,
    val2: str,
) -> FieldComparisonResult:
    """
    Compares two individual string values from an address field.
    """

    similarity: float
    ops = None

    similarity = ratio(val1, val2) * 100
    similarity = distance(val1, val2)
    ops = editops(val1, val2)

    return FieldComparisonResult(
        value1=val1,
        value2=val2,
        similarity_ratio=similarity,
        edit_operations=ops,
    )


def compare_addresses(
    addr1: Address,
    addr2: Address,
    field_weights: dict[str, float] = DEFAULT_FIELD_WEIGHTS,
) -> AddressComparisonResult:
    """
    Compares two Address objects field by field and computes an overall similarity score.
    """

    field_comparison_results = []
    total_weighted_score_sum = 0.0
    total_effective_weight = 0.0

    # Calculate score for each field
    ADDRESS_FIELD_NAMES = fields(Address)

    # Use the provided weights or default to the predefined weights
    for field_name in ADDRESS_FIELD_NAMES:
        val1 = getattr(addr1, field_name, None)
        val2 = getattr(addr2, field_name, None)

        field_result = _compare_single_field(val1, val2)
        field_comparison_results.append(field_result)

    address_results = FieldResults(*field_comparison_results)

    return AddressComparisonResult(
        address1=addr1,
        address2=addr2,
        field_comparisons=field_comparison_results,
    )
