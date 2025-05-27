from attrs import define, fields
from Levenshtein import distance, editops, ratio

from .models import Address, AddressComparisonResult, FieldComparisonResult
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
    field_weights: Optional[Dict[str, float]] = None,
) -> AddressComparisonResult:
    """
    Compares two Address objects field by field and computes an overall similarity score.
    """
    current_weights = field_weights if field_weights is not None else DEFAULT_FIELD_WEIGHTS

    field_comparison_results: List[FieldComparisonResult] = []
    total_weighted_score_sum = 0.0
    total_effective_weight = 0.0

    for field_name in ADDRESS_FIELD_NAMES:
        val1 = getattr(addr1, field_name, None)
        val2 = getattr(addr2, field_name, None)

        field_result = _compare_single_field(field_name, val1, val2)
        field_comparison_results.append(field_result)

        weight = current_weights.get(field_name, 0.0)

        # Only include fields in weighted average if they have data in at least one address
        # and have a non-zero weight.
        # Fields where both values are None get a similarity of 1.0 for that field,
        # but they don't contribute to the weighted average unless you want them to.
        # Current logic: if a field is None in both, it doesn't affect the overall score's
        # denominator (total_effective_weight).
        if (norm_val1_temp := normalize_string(val1)) is not None and (
            norm_val2_temp := normalize_string(val2)
        ) is not None:
            # Both have some content (or are empty strings, handled by _compare_single_field)
            total_weighted_score_sum += field_result.similarity_ratio * weight
            total_effective_weight += weight
        elif not (norm_val1_temp is None and norm_val2_temp is None):
            # One has content, the other is None (or empty string vs content)
            total_weighted_score_sum += field_result.similarity_ratio * weight  # ratio will be 0
            total_effective_weight += weight

    overall_similarity: float
    if total_effective_weight == 0:
        # This can happen if:
        # 1. Both addresses are completely empty (all fields None).
        # 2. All fields with actual data have zero weight assigned.
        is_addr1_empty = all(getattr(addr1, f, None) is None for f in ADDRESS_FIELD_NAMES)
        is_addr2_empty = all(getattr(addr2, f, None) is None for f in ADDRESS_FIELD_NAMES)
        if is_addr1_empty and is_addr2_empty:
            overall_similarity = 1.0
        else:
            # No basis for weighted comparison or one/both effectively empty for weighted fields
            overall_similarity = 0.0
    else:
        overall_similarity = total_weighted_score_sum / total_effective_weight

    return AddressComparisonResult(
        address1=addr1,
        address2=addr2,
        overall_similarity_score=max(0.0, min(1.0, overall_similarity)),  # Clamp to [0,1]
        field_comparisons=field_comparison_results,
    )
