import pytest
from app.views.calculators.percentage import PercentageCalculator
import tkinter as tk


class TestPercentageCalculatorIntegration:
    @pytest.fixture
    def calculator(self):
        root = tk.Tk()
        frame = tk.Frame(root)
        user = MagicMock()
        calculator = PercentageCalculator(frame, user)
        yield calculator
        root.destroy()

    def test_full_flow(self, calculator):
        # Set test values
        calculator.obtained_var.set(85)
        calculator.total_var.set(100)

        # Perform calculation
        calculator.calculate_percentage()

        # Check results
        result_widgets = calculator.results_frame.winfo_children()
        assert len(result_widgets) > 0

        # Verify chart was created
        canvas_widgets = [w for w in result_widgets if "FigureCanvasTkAgg" in str(w)]
        assert len(canvas_widgets) == 1

        # Verify percentage text
        result_labels = [w for w in result_widgets
                         if isinstance(w, tk.Label) and "85.00%" in w.cget("text")]
        assert len(result_labels) == 1