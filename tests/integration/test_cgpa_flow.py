import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
from app.views.calculators.cgpa import CGPACalculator


class TestCGPACalculatorIntegration:
    @pytest.fixture
    def calculator(self):
        root = tk.Tk()
        root.withdraw()  # Prevent window from showing during tests
        frame = tk.Frame(root)
        user = MagicMock()
        calculator = CGPACalculator(frame, user)
        yield calculator
        root.destroy()

    def find_cgpa_label(self, parent):
        """Recursively search for the CGPA label in all child widgets"""
        for child in parent.winfo_children():
            if isinstance(child, tk.Label) and "CGPA" in child.cget("text"):
                return child
            result = self.find_cgpa_label(child)
            if result:
                return result
        return None

    def test_full_calculation_flow(self, calculator):
        """Test the complete CGPA calculation flow with actual calculations"""
        # Setup test data
        calculator.semesters[0]["sgpa"].set(3.5)
        calculator.semesters[0]["credits"].set(15)
        calculator.semesters[1]["sgpa"].set(3.8)
        calculator.semesters[1]["credits"].set(18)

        # Expected calculation
        expected_cgpa = (3.5 * 15 + 3.8 * 18) / (15 + 18)  # ~3.66

        # Perform calculation
        calculator.calculate_cgpa()

        # Update the UI and wait for changes
        calculator.parent.update()
        calculator.parent.update_idletasks()

        # Find the CGPA label recursively
        cgpa_label = self.find_cgpa_label(calculator.results_frame)
        assert cgpa_label is not None, "CGPA label not found in results frame"
        assert f"{expected_cgpa:.2f}" in cgpa_label.cget("text")

    def test_calculation_with_mock(self, calculator):
        """Test the UI-service integration with mocked calculation"""
        # Setup test data
        calculator.semesters[0]["sgpa"].set(3.5)
        calculator.semesters[0]["credits"].set(15)
        calculator.semesters[1]["sgpa"].set(3.8)
        calculator.semesters[1]["credits"].set(18)

        with patch('app.views.calculators.cgpa.calculate_cgpa') as mock_calculate:
            mock_calculate.return_value = (3.66, [])  # Mocked return value

            calculator.calculate_cgpa()

            # Verify service was called with correct data
            called_data = mock_calculate.call_args[0][0]
            assert len(called_data) == 2
            assert called_data[0]['sgpa'] == 3.5
            assert called_data[0]['credits'] == 15
            assert called_data[1]['sgpa'] == 3.8
            assert called_data[1]['credits'] == 18

            # Update the UI and wait for changes
            calculator.parent.update()
            calculator.parent.update_idletasks()

            # Find the CGPA label recursively
            cgpa_label = self.find_cgpa_label(calculator.results_frame)
            assert cgpa_label is not None, "CGPA label not found in results frame"
            assert "3.66" in cgpa_label.cget("text")