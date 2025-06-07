import pytest
from app.services.conversion import convert_grade, ConversionError

def test_convert_grade_percentage_to_grade_and_gpa():
    results = convert_grade(percentage=85)
    assert results['grade'] == 'B'
    assert results['gpa'] == 3.0

def test_convert_grade_grade_to_percentage_and_gpa():
    results = convert_grade(grade='A')
    assert results['percentage'] == 100.0
    assert results['gpa'] == 4.0

def test_convert_grade_gpa_to_grade_and_percentage():
    results = convert_grade(gpa=3.5)
    assert results['grade'] == 'B+'
    assert results['percentage'] == 87.5

def test_invalid_percentage():
    with pytest.raises(ConversionError):
        convert_grade(percentage='invalid')

def test_invalid_grade():
    with pytest.raises(ConversionError):
        convert_grade(grade='Z')

def test_invalid_gpa():
    with pytest.raises(ConversionError):
        convert_grade(gpa='invalid')
