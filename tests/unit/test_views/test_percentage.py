import pytest
from unittest.mock import MagicMock
from app.views.calculators.percentage import PercentageCalculator
import tkinter as tk


class TestPercentageCalculatorUI:
    @pytest.fixture
    def calculator(self):
        root = tk.Tk()
        frame = tk.Frame(root)
        user = MagicMock()
        calculator = PercentageCalculator(frame, user)
        yield calculator
        root.destroy()

    def test_initial_setup(self, calculator):
        assert calculator.obtained_var.get() == 0.0
        assert calculator.total_var.get() == 100.0

    def test_validate_number(self, calculator):
        assert calculator.validate_number("100") is True
        assert calculator.validate_number("0") is True
        assert calculator.validate_number("75.5") is True
        assert calculator.validate_number("-10") is False
        assert calculator.validate_number("abc") is False
        assert calculator.validate_number("") is True

    @pytest.mark.parametrize("obtained,total,expected", [
        (75, 100, 75.0),
        (50, 200, 25.0),
        (30, 40, 75.0),
        (0, 100, 0.0)
    ])
    def test_calculate_percentage(self, calculator, obtained, total, expected):
        calculator.obtained_var.set(obtained)
        calculator.total_var.set(total)
        calculator.calculate_percentage()

        # Verify result label exists with expected text
        result_labels = [w for w in calculator.results_frame.winfo_children()
                         if isinstance(w, tk.Label) and f"{expected:.2f}%" in w.cget("text")]
        assert len(result_labels) == 1

    def test_zero_total_marks(self, calculator):
        calculator.obtained_var.set(50)
        calculator.total_var.set(0)

        with pytest.raises(ValueError):
            calculator.calculate_percentage()