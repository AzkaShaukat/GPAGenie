import pytest
from app.constants.grades import GRADE_POINTS, PERCENTAGE_RANGES, INTERNATIONAL_GRADES


class TestGradeStandards:
    def test_grade_points(self):
        assert GRADE_POINTS['A'] == 4.0
        assert GRADE_POINTS['B+'] == 3.3
        assert GRADE_POINTS['C-'] == 1.7
        assert GRADE_POINTS['F'] == 0.0

    def test_percentage_ranges(self):
        assert PERCENTAGE_RANGES['A'] == (93, 96)
        assert PERCENTAGE_RANGES['B-'] == (80, 82)
        assert PERCENTAGE_RANGES['D+'] == (67, 69)

    def test_international_grades(self):
        assert INTERNATIONAL_GRADES['UK']['First Class'] == 4.0
        assert INTERNATIONAL_GRADES['Europe']['B'] == 3.0
        assert INTERNATIONAL_GRADES['Europe']['E'] == 0.5

    def test_grade_points_completeness(self):
        for letter in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']:
            assert letter in GRADE_POINTS

    def test_percentage_ranges_consistency(self):
        # Verify ranges don't overlap and are in descending order
        ranges = list(PERCENTAGE_RANGES.values())
        for i in range(len(ranges) - 1):
            assert ranges[i][0] > ranges[i + 1][1]