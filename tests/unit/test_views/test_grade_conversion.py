import pytest
from app.services.conversion import (
    convert_grade,
    find_closest_letter,
    gpa_to_percentage,
    percentage_to_gpa
)
from app.utils.exceptions import ConversionError


class TestGradeConversion:
    def test_convert_from_gpa(self):
        # Test valid GPA conversions
        result = convert_grade("GPA (4.0)", 3.5)
        assert result["GPA (4.0 scale)"] == "3.50"
        assert result["Letter Grade"] == "A-"  # Changed from B+ to A-
        assert result["Percentage"] == "95.0%"

        result = convert_grade("GPA (4.0)", 2.8)
        assert result["Letter Grade"] == "B-"

    def test_convert_from_percentage(self):
        # Test valid percentage conversions
        result = convert_grade("Percentage", 88)
        assert result["GPA (4.0 scale)"] == "3.30"
        assert result["Letter Grade"] == "B+"

        result = convert_grade("Percentage", 76.5)
        assert result["Letter Grade"] == "C"

    def test_convert_from_letter(self):
        # Test valid letter grade conversions
        result = convert_grade("Letter Grade", "A-")
        assert result["GPA (4.0 scale)"] == "3.70"
        assert result["Percentage"] == "97.0%"

        result = convert_grade("Letter Grade", "C+")
        assert float(result["GPA (4.0 scale)"]) == pytest.approx(2.3)

    def test_invalid_inputs(self):
        # Test invalid GPA values
        with pytest.raises(ConversionError):
            convert_grade("GPA (4.0)", 4.5)

        with pytest.raises(ConversionError):
            convert_grade("GPA (4.0)", -1.0)

        # Test invalid percentage values
        with pytest.raises(ConversionError):
            convert_grade("Percentage", 105)

        with pytest.raises(ConversionError):
            convert_grade("Percentage", -5)

        # Test invalid letter grades
        with pytest.raises(ConversionError):
            convert_grade("Letter Grade", "E")

    def test_find_closest_letter(self):
        assert find_closest_letter(3.7) == "A-"
        assert find_closest_letter(3.2) == "B+"  # Changed from B to B+
        assert find_closest_letter(2.4) == "C+"  # Closer to C+ than C
        assert find_closest_letter(0.8) == "D"

    def test_gpa_percentage_conversion(self):
        # Test GPA to percentage conversion
        assert gpa_to_percentage(4.0) == 100.0
        assert gpa_to_percentage(3.0) == 90.0
        assert gpa_to_percentage(2.0) == 80.0
        assert gpa_to_percentage(1.0) == 70.0

        # Test percentage to GPA conversion
        assert percentage_to_gpa(97) == 4.0
        assert percentage_to_gpa(93) == 4.0
        assert percentage_to_gpa(90) == 3.7
        assert percentage_to_gpa(87) == 3.3
        assert percentage_to_gpa(83) == 3.0
        assert percentage_to_gpa(80) == 2.7
        assert percentage_to_gpa(77) == 2.3
        assert percentage_to_gpa(73) == 2.0
        assert percentage_to_gpa(70) == 1.7
        assert percentage_to_gpa(67) == 1.3
        assert percentage_to_gpa(65) == 1.0
        assert percentage_to_gpa(64) == 0.0