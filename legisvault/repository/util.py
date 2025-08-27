import re
import string
from django import template
import os


#Generating Publication Number series
def generate_resolution_number(base_number=None):

    """
    Generate the next resolution number.
    - If base_number is None: generate a new base like '2025-01'
    - If base_number is given: generate variant like '2025-01A', '2025-01B', etc.
    """
    from .models import LegalMeasure  # import your model here
    from datetime import date

    current_year = date.today().year

    if base_number:
        # Create variant of existing number like '2025-01A', '2025-01B', etc.
        existing = LegalMeasure.objects.filter(number__startswith=base_number)
        suffixes = [
            match.group(1)
            for res in existing
            if (match := re.match(rf"^{base_number}([A-Z])?$", res.number))
            and match.group(1)
        ]

        if not suffixes:
            return f"{base_number}A"  # Start with A if none exist

        last = max(suffixes, key=lambda s: string.ascii_uppercase.index(s))
        next_letter = string.ascii_uppercase[string.ascii_uppercase.index(last) + 1]
        return f"{base_number}{next_letter}"

    else:
        # Generate new base number for the year, like '2025-01'
        resolutions = LegalMeasure.objects.filter(number__startswith=str(current_year))
        base_numbers = [
            int(match.group(1))
            for res in resolutions
            if (match := re.match(rf"^{current_year}-(\d+)", res.number))
        ]

        next_base = max(base_numbers) + 1 if base_numbers else 1
        return f"{current_year}-{str(next_base).zfill(2)}"
    





