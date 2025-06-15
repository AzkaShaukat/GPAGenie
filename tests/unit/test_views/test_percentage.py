import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
from app.views.calculators.percentage import PercentageCalculator


class TestPercentageCalculatorUI:
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
        calculator = PercentageCalculator(frame, user)
        yield calculator
        try:
            root.destroy()
        except tk.TclError:
            pass

    def test_initial_setup(self, calculator):
        """Test that initial values are set correctly"""
        assert calculator.obtained_var.get() == 0.0
        assert calculator.total_var.get() == 100.0

    def test_validate_number(self, calculator):
        """Test input validation works correctly"""
        assert calculator.validate_number("100") is True
        assert calculator.validate_number("0") is True
        assert calculator.validate_number("75.5") is True
        assert calculator.validate_number("-10") is False
        assert calculator.validate_number("abc") is False
        assert calculator.validate_number("") is True

    def test_zero_total_marks(self, calculator):
        """Test that zero total marks shows error message"""
        calculator.obtained_var.set(50)
        calculator.total_var.set(0)

        # Patch messagebox to prevent GUI popup during test
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            calculator.calculate_percentage()
            # Verify error message was shown
            assert mock_showerror.call_count == 1
            args = mock_showerror.call_args[0]
            assert args[0] == "Calculation Error"
            assert "Total marks cannot be zero" in args[1]