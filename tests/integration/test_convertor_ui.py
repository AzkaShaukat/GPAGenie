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
    #
    # def test_input_field_updates(self, converter):
    #     # Test changing the conversion type updates input fields
    #     converter.convert_from.set("Percentage")
    #     converter.update_input_fields()
    #     assert len(converter.input_frame.winfo_children()) > 0
    #
    #     converter.convert_from.set("Letter Grade")
    #     converter.update_input_fields()
    #     assert len(converter.input_frame.winfo_children()) > 0


