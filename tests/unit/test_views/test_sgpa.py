import pytest
from unittest.mock import MagicMock, patch
from app.views.calculators.sgpa import SGPACalculator
import tkinter as tk


class TestSGPACalculatorUI:
    @pytest.fixture
    def calculator(self):
        root = tk.Tk()
        frame = tk.Frame(root)
        calculator = SGPACalculator(frame, user=None)
        yield calculator
        root.destroy()

    def test_initial_subjects(self, calculator):
        assert len(calculator.subjects) == 3

    def test_add_subject(self, calculator):
        initial_count = len(calculator.subjects)
        calculator.add_subject_row()
        assert len(calculator.subjects) == initial_count + 1

    @patch('app.services.calculations.calculate_sgpa')
    def test_calculate_sgpa(self, mock_calc, calculator):
        mock_calc.return_value = (3.5, [])

        # Simulate entering data
        calculator.subjects[0]["grade"].set("A")
        calculator.subjects[0]["credits"].set(3)

        calculator.calculate_sgpa()

        mock_calc.assert_called_once()
        assert len(calculator.results_frame.winfo_children()) > 0