import pytest
from app.services.calculations import calculate_sgpa
from app.views.calculators.sgpa import SGPACalculator
import tkinter as tk


class TestSGPACalculatorIntegration:
    @pytest.fixture
    def calculator(self):
        root = tk.Tk()
        frame = tk.Frame(root)
        calculator = SGPACalculator(frame, user=None)
        yield calculator
        root.destroy()

    def test_full_calculation_flow(self, calculator):
        # Set up test data
        calculator.subjects[0]["grade"].set("A")
        calculator.subjects[0]["credits"].set(4)

        calculator.subjects[1]["grade"].set("B")
        calculator.subjects[1]["credits"].set(3)

        # Perform calculation
        calculator.calculate_sgpa()

        # Check results frame was populated
        result_widgets = calculator.results_frame.winfo_children()
        assert len(result_widgets) > 0

        # Check for result label
        result_labels = [w for w in result_widgets if isinstance(w, tk.Label) and "SGPA" in w.cget("text")]
        assert len(result_labels) == 1