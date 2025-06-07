import pytest
from app.services.calculations import calculate_sgpa, GRADE_POINTS


class TestSGPACalculations:
    def test_calculate_sgpa_basic(self):
        subjects = [
            {"subject": "Math", "grade": "A", "credits": 3},
            {"subject": "Physics", "grade": "B", "credits": 4}
        ]

        sgpa, results = calculate_sgpa(subjects)

        expected_sgpa = (4.0 * 3 + 3.0 * 4) / (3 + 4)
        assert sgpa == pytest.approx(expected_sgpa)
        assert len(results) == 2
        assert results[0][1] == 4.0
        assert results[1][1] == 3.0

    def test_calculate_sgpa_empty(self):
        with pytest.raises(ValueError):
            calculate_sgpa([])

    def test_calculate_sgpa_invalid_grade(self):
        subjects = [{"subject": "Math", "grade": "X", "credits": 3}]
        with pytest.raises(ValueError):
            calculate_sgpa(subjects)

    def test_calculate_sgpa_invalid_credits(self):
        subjects = [{"subject": "Math", "grade": "A", "credits": 0}]
        with pytest.raises(ValueError):
            calculate_sgpa(subjects)

    def test_all_grades_defined(self):
        test_grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]
        for grade in test_grades:
            subjects = [{"subject": "Test", "grade": grade, "credits": 1}]
            sgpa, _ = calculate_sgpa(subjects)
            assert sgpa == GRADE_POINTS[grade]


import pytest
from app.services.calculations import calculate_cgpa

class TestCGPACalculations:
    def test_basic_cgpa(self):
        semesters = [
            {'name': 'Sem 1', 'sgpa': 3.5, 'credits': 15},
            {'name': 'Sem 2', 'sgpa': 3.8, 'credits': 18}
        ]
        cgpa, results = calculate_cgpa(semesters)
        assert cgpa == pytest.approx((3.5*15 + 3.8*18)/(15+18))
        assert len(results) == 2

    def test_empty_semesters(self):
        with pytest.raises(ValueError):
            calculate_cgpa([])

    def test_zero_credits(self):
        with pytest.raises(ValueError):
            calculate_cgpa([{'name': 'Sem 1', 'sgpa': 3.5, 'credits': 0}])