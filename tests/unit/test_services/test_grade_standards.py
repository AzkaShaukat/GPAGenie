from app.utils.constants import GRADE_TO_GPA

def test_grade_standards():
    assert 'A' in GRADE_TO_GPA
    assert GRADE_TO_GPA['B'] == 3.0
    assert GRADE_TO_GPA['C+'] == 2.3
    assert GRADE_TO_GPA['F'] == 0.0
