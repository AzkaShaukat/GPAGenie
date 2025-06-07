import pytest
from unittest.mock import MagicMock
from app.views.calculators.cgpa import CGPACalculator
import tkinter as tk

class TestCGPACalculatorUI:
    @pytest.fixture
    def calculator(self):
        root = tk.Tk()
        frame = tk.Frame(root)
        user = MagicMock()
        calculator = CGPACalculator(frame, user)
        yield calculator
        root.destroy()

    def test_initial_semesters(self, calculator):
        assert len(calculator.semesters) == 2

    def test_add_semester(self, calculator):
        initial_count = len(calculator.semesters)
        calculator.add_semester_row()
        assert len(calculator.semesters) == initial_count + 1

    def test_validate_grade_valid(self, calculator):
        assert calculator.validate_grade("3.5") is True
        assert calculator.validate_grade("0.0") is True
        assert calculator.validate_grade("4.0") is True
        assert calculator.validate_grade("") is True

    def test_validate_grade_invalid(self, calculator):
        assert calculator.validate_grade("-1.0") is False
        assert calculator.validate_grade("4.1") is False
        assert calculator.validate_grade("abc") is False