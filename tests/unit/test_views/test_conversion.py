import pytest
from app.services.conversion import convert_grade, ConversionError

def test_convert_grade_percentage_to_grade_and_gpa():
    results = convert_grade(convert_from="Percentage", value=85)
    assert results['Letter Grade'] == 'B'
    assert float(results['GPA (4.0 scale)']) == pytest.approx(3.0)

def test_convert_grade_grade_to_percentage_and_gpa():
    results = convert_grade(convert_from="Letter Grade", value='A')
    assert float(results['Percentage'][:-1]) == pytest.approx(100.0)  # Remove '%' and convert to float
    assert float(results['GPA (4.0 scale)']) == pytest.approx(4.0)

def test_convert_grade_gpa_to_grade_and_percentage():
    results = convert_grade(convert_from="GPA (4.0)", value=3.5)
    assert results['Letter Grade'] == 'A-'
    assert float(results['Percentage'][:-1]) == pytest.approx(95)  # Remove '%' and convert to float

def test_invalid_percentage():
    with pytest.raises(ConversionError):
        convert_grade(convert_from="Percentage", value='invalid')

def test_invalid_grade():
    with pytest.raises(ConversionError):
        convert_grade(convert_from="Letter Grade", value='Z')

def test_invalid_gpa():
    with pytest.raises(ConversionError):
        convert_grade(convert_from="GPA (4.0)", value='invalid')