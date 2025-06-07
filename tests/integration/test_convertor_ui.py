import pytest
from tkinter import Tk
from app.views.calculators.converter import GradeConverter
from app.services.conversion import convert_grade


class TestConverterUI:
    @pytest.fixture
    def converter(self):
        root = Tk()
        root.withdraw()  # Hide the main window
        converter = GradeConverter(root)
        yield converter
        root.destroy()

    def test_ui_initialization(self, converter):
        assert converter.main_frame.winfo_exists() == 1
        assert converter.convert_from.get() == "GPA (4.0)"

    def test_input_field_updates(self, converter):
        # Test changing the conversion type updates input fields
        converter.convert_from.set("Percentage")
        converter.update_input_fields()
        assert len(converter.input_frame.winfo_children()) > 0

        converter.convert_from.set("Letter Grade")
        converter.update_input_fields()
        assert len(converter.input_frame.winfo_children()) > 0

    def test_validation(self, converter):
        # Test GPA validation
        converter.convert_from.set("GPA (4.0)")
        converter.update_input_fields()
        converter.input_var.set(5.0)  # Invalid GPA
        assert converter.validate_input("5.0") is False

        # Test percentage validation
        converter.convert_from.set("Percentage")
        converter.update_input_fields()
        converter.input_var.set(110)  # Invalid percentage
        assert converter.validate_input("110") is False

    def test_conversion_flow(self, converter, monkeypatch):
        # Mock the conversion service
        def mock_convert(convert_from, value):
            return {
                "GPA (4.0 scale)": "3.50",
                "Letter Grade": "B+",
                "Percentage": "87.5%"
            }

        monkeypatch.setattr("app.services.conversion.convert_grade", mock_convert)

        # Set up UI state
        converter.convert_from.set("GPA (4.0)")
        converter.update_input_fields()
        converter.input_var.set(3.5)

        # Trigger conversion
        converter.perform_conversion()

        # Verify results are displayed
        assert len(converter.output_frame.winfo_children()) > 0