import pytest
from unittest.mock import MagicMock, patch
from app.views.calculators.sgpa import SGPACalculator
import tkinter as tk


class TestSGPACalculatorUI:
    @pytest.fixture
    def calculator(self):
        # Workaround for Tkinter issues in tests
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the window during tests
        except tk.TclError:
            pytest.skip("Tkinter not properly installed")

        frame = tk.Frame(root)
        user = MagicMock()
        calculator = SGPACalculator(frame, user)
        yield calculator
        try:
            root.destroy()
        except tk.TclError:
            pass

    def test_initial_subjects(self, calculator):
        """Test that calculator initializes with 3 subject rows"""
        assert len(calculator.subjects) == 3

    def test_add_subject(self, calculator):
        """Test that adding a subject row works"""
        initial_count = len(calculator.subjects)
        calculator.add_subject_row()
        assert len(calculator.subjects) == initial_count + 1

    @patch('app.views.calculators.sgpa.calculate_sgpa')
    def test_calculate_sgpa(self, mock_calc, calculator):
        """Test that SGPA calculation works with valid inputs"""
        # Setup mock return value
        mock_calc.return_value = (3.5, [])

        # Simulate entering data for all required fields
        for subject in calculator.subjects:
            subject["grade"].set("A")
            subject["credits"].set(3)

        # Perform calculation
        calculator.calculate_sgpa()

        # Verify calculation was called
        assert mock_calc.call_count == 1

        # Verify results frame was populated
        assert len(calculator.results_frame.winfo_children()) > 0