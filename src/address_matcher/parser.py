import re
from typing import Optional

from .exceptions import ParsingError
from .models import Address

# Regex to find a 4-digit zipcode (Belgium specific)
RE_BELGIAN_ZIPCODE = r"\b(\d{4})\b"
# Basic regex for street number (digits, maybe a letter, maybe bis/ter or /)
RE_STREET_NUMBER = r"\b(\d+[a-zA-Z]*(?:\s*(?:bis|ter))?(?:\s*/\s*\d*)?)\b"


def parse_free_text_address(text: str, default_country: str = "Belgium") -> Address:
    """
    Parses a free-text address string into a structured Address object.

    DISCLAIMER: This is a VERY basic placeholder parser. It uses simple
    regexes and heuristics that will likely fail on many real-world
    Belgian addresses. It does not handle multiple languages well,
    complex street names, or various address formats robustly.
    For production use, a much more sophisticated parsing solution is required.
    """
    original_text = text
    text = text.strip()

    street_name: Optional[str] = None
    street_number: Optional[str] = None
    box_number: Optional[str] = None  # Placeholder: box number parsing not implemented
    zipcode: Optional[str] = None
    city: Optional[str] = None

    # 1. Attempt to extract zipcode
    zip_match = re.search(RE_BELGIAN_ZIPCODE, text)
    processed_text = text
    if zip_match:
        zipcode = zip_match.group(1)
        # Try to get city: often after zipcode, or text after zipcode string
        # This is highly heuristic.
        text_around_zip = text[: zip_match.start()] + " " + text[zip_match.end() :]
        parts = [p.strip() for p in text_around_zip.split(",") if p.strip()]

        # Simplistic city extraction: assumes city might be near zipcode
        # or the largest non-numeric part.
        potential_city_parts = []
        if len(text[zip_match.end() :].strip()) > 0:
            potential_city_parts.append(text[zip_match.end() :].strip().split(",")[0].strip())

        # Fallback: try to find a non-numeric part that could be city
        # This is very naive. A list of Belgian cities would be better.
        candidate_cities = [p for p in parts if not p.isdigit() and not re.search(r"\d", p)]  # no digits
        if candidate_cities:
            city = candidate_cities[-1]  # Take the last one as a guess
            # Remove city from processed_text to avoid re-parsing
            processed_text = processed_text.replace(city, "").strip().rstrip(",")
        elif potential_city_parts:
            city = potential_city_parts[0]
            processed_text = processed_text.replace(city, "").strip().rstrip(",")

        processed_text = processed_text.replace(zipcode, "").strip()

    # 2. Attempt to extract street number from the remaining text
    # Search from right to left, as numbers are often at the end of street part
    num_matches = list(re.finditer(RE_STREET_NUMBER, processed_text))
    if num_matches:
        # Assume the last number found is the street number
        last_num_match = num_matches[-1]
        street_number = last_num_match.group(0).strip()

        # Assume street name is everything before the last number or after if number is first
        sn_part1 = processed_text[: last_num_match.start()].strip()
        sn_part2 = processed_text[last_num_match.end() :].strip()

        if sn_part1 and not sn_part2:  # Number at the end
            street_name = sn_part1.rstrip(",")
        elif sn_part2 and not sn_part1:  # Number at the beginning
            street_name = sn_part2.rstrip(",")
        elif sn_part1 and sn_part2:  # Number in middle, or parts on both sides
            street_name = (sn_part1 + " " + sn_part2).strip().rstrip(",")
        elif sn_part1:
            street_name = sn_part1.rstrip(",")
        elif sn_part2:
            street_name = sn_part2.rstrip(",")
        else:  # Only number was found
            street_name = None

        if street_name:
            street_name = re.sub(r"\s+,", ",", street_name)  # Clean " ,"
            street_name = street_name.strip()

    else:  # No number found
        street_name = processed_text.strip().rstrip(",")

    # Final cleanup for street_name if it's the only thing left
    if not street_number and not zipcode and not city and original_text and not street_name:
        street_name = original_text  # Fallback if nothing else parsed

    # If street_name contains city and they were not separated
    if street_name and city and city in street_name:
        street_name = street_name.replace(city, "").strip().rstrip(",")

    # Basic check if parsing yielded anything
    if not any([street_name, street_number, zipcode, city]):
        # If you want to be strict:
        # raise ParsingError(f"Could not parse address: {original_text}")
        # For now, return potentially empty fields.
        pass

    return Address(
        street_name=street_name if street_name else None,
        street_number=street_number if street_number else None,
        box_number=box_number,  # Not implemented
        zipcode=zipcode if zipcode else None,
        city=city if city else None,
        country=default_country,
    )
