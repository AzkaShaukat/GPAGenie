import pytest
from app.views.calculators.cgpa import CGPACalculator
from app.services.calculations import calculate_cgpa
import tkinter as tk

class TestCGPACalculatorIntegration:
    @pytest.fixture
    def calculator(self):
        root = tk.Tk()
        frame = tk.Frame(root)
        user = MagicMock()
        calculator = CGPACalculator(frame, user)
        yield calculator
        root.destroy()

    def test_full_calculation_flow(self, calculator):
        # Simulate entering data
        calculator.semesters[0]["sgpa"].set(3.5)
        calculator.semesters[0]["credits"].set(15)
        calculator.semesters[1]["sgpa"].set(3.8)
        calculator.semesters[1]["credits"].set(18)

        # Perform calculation
        calculator.calculate_cgpa()

        # Check results frame was populated
        result_widgets = calculator.results_frame.winfo_children()
        assert len(result_widgets) > 0

        # Check for result label
        result_labels = [w for w in result_widgets
                        if isinstance(w, tk.Label) and "CGPA" in w.cget("text")]
        assert len(result_labels) == 1