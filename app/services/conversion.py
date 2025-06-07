from typing import Dict
from app.utils.exceptions import ConversionError

# Standard conversion tables
LETTER_TO_GPA = {
    'A+': 4.0,
    'A': 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1.0,
    'F': 0.0
}

GPA_TO_LETTER = {
    4.0: 'A',
    3.7: 'A-',
    3.3: 'B+',
    3.0: 'B',
    2.7: 'B-',
    2.3: 'C+',
    2.0: 'C',
    1.7: 'C-',
    1.3: 'D+',
    1.0: 'D',
    0.0: 'F'
}


# In app/services/conversion.py
def convert_grade(convert_from: str, value) -> Dict[str, str]:
    """Convert between grade formats (GPA, percentage, letter)"""
    try:
        # Handle empty/blank values
        if value is None or str(value).strip() == "":
            raise ConversionError("Please enter a value to convert")

        if convert_from == "GPA (4.0)":
            try:
                gpa = float(value)
            except ValueError:
                raise ConversionError("GPA must be a number")

            if not 0.0 <= gpa <= 4.0:
                raise ConversionError("GPA must be between 0.0 and 4.0")

            letter = find_closest_letter(gpa)
            percentage = gpa_to_percentage(gpa)

        elif convert_from == "Percentage":
            try:
                percentage = float(value)
            except ValueError:
                raise ConversionError("Percentage must be a number")

            if not 0.0 <= percentage <= 100.0:
                raise ConversionError("Percentage must be between 0 and 100")

            gpa = percentage_to_gpa(percentage)
            letter = find_closest_letter(gpa)

        elif convert_from == "Letter Grade":
            letter = value.upper().strip()
            if letter not in LETTER_TO_GPA:
                raise ConversionError(f"Invalid letter grade: {value}")

            gpa = LETTER_TO_GPA[letter]
            percentage = gpa_to_percentage(gpa)

        else:
            raise ConversionError(f"Unknown conversion type: {convert_from}")

        return {
            "GPA (4.0 scale)": f"{gpa:.2f}",
            "Letter Grade": letter,
            "Percentage": f"{percentage:.1f}%"
        }

    except ConversionError:
        raise
    except Exception as e:
        raise ConversionError(f"Conversion failed: {str(e)}")
def find_closest_letter(gpa: float) -> str:
    """Find the closest letter grade for a given GPA"""
    # Handle edge cases
    if gpa >= 4.0:
        return 'A'
    if gpa <= 0.0:
        return 'F'

    # Find closest GPA in the conversion table
    closest_gpa = min(GPA_TO_LETTER.keys(), key=lambda x: abs(x - gpa))
    return GPA_TO_LETTER[closest_gpa]


def gpa_to_percentage(gpa: float) -> float:
    """Convert GPA to approximate percentage"""
    # Linear approximation (adjustable based on institution)
    return 60 + (gpa * 10) if gpa > 0 else 0


def percentage_to_gpa(percentage: float) -> float:
    """Convert percentage to approximate GPA"""
    # Linear approximation (adjustable based on institution)
    if percentage >= 97: return 4.0
    if percentage >= 93: return 4.0
    if percentage >= 90: return 3.7
    if percentage >= 87: return 3.3
    if percentage >= 83: return 3.0
    if percentage >= 80: return 2.7
    if percentage >= 77: return 2.3
    if percentage >= 73: return 2.0
    if percentage >= 70: return 1.7
    if percentage >= 67: return 1.3
    if percentage >= 65: return 1.0
    return 0.0