from address_matcher import Address, compare_addresses, parse_free_text_address

# Example with structured input
addr1_structured = Address(
    street_name="Rue de la Loi", street_number="16", zipcode="1000", city="Bruxelles", country="Belgium"
)
addr2_structured = Address(
    street_name="Wetstraat",  # Different language for street name
    street_number="16",
    box_number="B2",  # Extra info
    zipcode="1000",
    city="Brussel",  # Different language for city
    country="Belgium",
)

comparison_result_structured = compare_addresses(addr1_structured, addr2_structured)
print(f"Overall Similarity (Structured): {comparison_result_structured.overall_similarity_score:.2f}")
for field_comp in comparison_result_structured.field_comparisons:
    print(
        f"  Field: {field_comp.field_name:<15} "
        f"S1: '{str(field_comp.value1)[:20]:<20}' "
        f"S2: '{str(field_comp.value2)[:20]:<20}' "
        f"Score: {field_comp.similarity_ratio:.2f} "
        f"EditOps: {field_comp.edit_operations}"
    )
print("-" * 20)

# Example with free-text input (using the basic parser)
addr_text1 = "16 Rue de la Loi, 1000 Bruxelles"
addr_text2 = "Wetstraat 16, Bus 3, Brussel 1000"

# Note: The basic parser will struggle with "Bus 3" and language differences.
parsed_addr1 = parse_free_text_address(addr_text1)
parsed_addr2 = parse_free_text_address(addr_text2)

print("\nParsed Address 1:")
print(f"  Street: {parsed_addr1.street_name}, Num: {parsed_addr1.street_number}")
print(f"  Zip: {parsed_addr1.zipcode}, City: {parsed_addr1.city}")

print("\nParsed Address 2:")
print(f"  Street: {parsed_addr2.street_name}, Num: {parsed_addr2.street_number}")
print(f"  Zip: {parsed_addr2.zipcode}, City: {parsed_addr2.city}")


if parsed_addr1 and parsed_addr2:  # Check if parsing yielded something
    comparison_result_parsed = compare_addresses(parsed_addr1, parsed_addr2)
    print(f"\nOverall Similarity (Parsed): {comparison_result_parsed.overall_similarity_score:.2f}")
    for field_comp in comparison_result_parsed.field_comparisons:
        print(
            f"  Field: {field_comp.field_name:<15} "
            f"S1: '{str(field_comp.value1)[:20]:<20}' "
            f"S2: '{str(field_comp.value2)[:20]:<20}' "
            f"Score: {field_comp.similarity_ratio:.2f} "
            f"EditOps: {field_comp.edit_operations}"
        )
