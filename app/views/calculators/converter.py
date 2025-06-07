import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from app.services.conversion import convert_grade
from app.utils.style import configure_styles
from app.utils.exceptions import ConversionError

LETTER_TO_GPA = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'F': 0.0
}

class GradeConverter:
    def __init__(self, parent_frame):
        self.parent = parent_frame

        # Main container
        self.main_frame = tk.Frame(parent_frame, bg="#f0f8ff")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Label(
            self.main_frame,
            text="Grade Converter",
            font=("Helvetica", 20, "bold"),
            bg="#f0f8ff",
            fg="#4b0082"
        )
        header.pack(pady=(0, 20))

        # Converter area
        converter_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        converter_frame.pack(expand=True)

        # Input selection
        input_frame = tk.Frame(converter_frame, bg="#f0f8ff")
        input_frame.pack(pady=10)

        tk.Label(
            input_frame,
            text="Convert From:",
            font=("Helvetica", 12),
            bg="#f0f8ff"
        ).grid(row=0, column=0, padx=5, sticky="e")

        self.convert_from = ttk.Combobox(
            input_frame,
            values=["GPA (4.0)", "Percentage", "Letter Grade"],
            state="readonly",
            font=("Helvetica", 12),
            width=15
        )
        self.convert_from.grid(row=0, column=1, padx=5)
        self.convert_from.set("GPA (4.0)")
        self.convert_from.bind("<<ComboboxSelected>>", self.update_input_fields)

        # Input value
        self.input_frame = tk.Frame(converter_frame, bg="#f0f8ff")
        self.input_frame.pack(pady=10)

        # Output frame (will be populated dynamically)
        self.output_frame = tk.Frame(converter_frame, bg="#f0f8ff")
        self.output_frame.pack(pady=20)

        # Button
        btn_frame = tk.Frame(converter_frame, bg="#f0f8ff")
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Convert",
            command=self.perform_conversion,
            style="Accent.TButton"
        ).pack()

        # Info section
        self.setup_info_section()

        # Initialize input fields
        self.update_input_fields()

    def update_input_fields(self, event=None):
        # Clear previous input widgets
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        # Create appropriate input based on selection
        convert_type = self.convert_from.get()

        tk.Label(
            self.input_frame,
            text=f"Enter {convert_type}:",
            font=("Helvetica", 12),
            bg="#f0f8ff"
        ).grid(row=0, column=0, padx=5, sticky="e")

        # In update_input_fields method
        if convert_type == "Letter Grade":
            self.input_var = tk.StringVar()
            ttk.Combobox(
                self.input_frame,
                textvariable=self.input_var,
                values=list(LETTER_TO_GPA.keys()),
                state="readonly",
                font=("Helvetica", 12),
                width=5
            ).grid(row=0, column=1, padx=5)
        else:
            self.input_var = tk.DoubleVar()
            ttk.Entry(
                self.input_frame,
                textvariable=self.input_var,
                font=("Helvetica", 12),
                width=10,
                validate="key",
                validatecommand=(self.parent.register(self.validate_input), '%P')
            ).grid(row=0, column=1, padx=5)

    # In app/views/calculators/converter.py
    def validate_input(self, value):
        """Validate that input is appropriate for the current conversion type"""
        if not value:
            return True

        convert_type = self.convert_from.get()

        try:
            if convert_type == "GPA (4.0)":
                num = float(value)
                return 0.0 <= num <= 4.0
            elif convert_type == "Percentage":
                num = float(value)
                return 0.0 <= num <= 100.0
            elif convert_type == "Letter Grade":
                return value.upper() in LETTER_TO_GPA
            return True
        except ValueError:
            return False

    def perform_conversion(self):
        # Clear previous results
        for widget in self.output_frame.winfo_children():
            widget.destroy()

        try:
            convert_type = self.convert_from.get()
            input_value = self.input_var.get()

            # Additional validation
            if not input_value:
                raise ConversionError("Please enter a value to convert")

            if convert_type == "Letter Grade" and input_value.upper() not in LETTER_TO_GPA:
                raise ConversionError(f"Invalid letter grade: {input_value}")

            results = convert_grade(convert_type, input_value)

            # Display results in a table format similar to reference table
            result_table = tk.Frame(self.output_frame, bg="#f0f8ff")
            result_table.pack(pady=10)

            # Header
            tk.Label(
                result_table,
                text="Conversion Results",
                font=("Helvetica", 12, "bold"),
                bg="#f0f8ff",
                fg="#4b0082"
            ).grid(row=0, columnspan=2, pady=(0, 10))

            # Results rows
            for row, (label, value) in enumerate(results.items(), start=1):
                tk.Label(
                    result_table,
                    text=label + ":",
                    font=("Helvetica", 11, "bold"),
                    bg="#f0f8ff"
                ).grid(row=row, column=0, padx=5, pady=2, sticky="e")

                tk.Label(
                    result_table,
                    text=value,
                    font=("Helvetica", 11),
                    bg="#f0f8ff"
                ).grid(row=row, column=1, padx=5, pady=2, sticky="w")

            # Create visualization
            self.create_conversion_chart(results)

        except ConversionError as e:
            messagebox.showerror("Conversion Error", str(e))
        # except Exception as e:
        #     # messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def perform_conversion(self):
        # Clear previous results
        for widget in self.output_frame.winfo_children():
            widget.destroy()

        try:
            convert_type = self.convert_from.get()
            input_value = self.input_var.get()

            if not input_value:
                raise ConversionError("Please enter a value to convert")

            results = convert_grade(convert_type, input_value)

            # Display results
            tk.Label(
                self.output_frame,
                text="Conversion Results:",
                font=("Helvetica", 14, "bold"),
                bg="#f0f8ff",
                fg="#4b0082"
            ).pack(pady=(0, 10))

            result_grid = tk.Frame(self.output_frame, bg="#f0f8ff")
            result_grid.pack()

            for i, (label, value) in enumerate(results.items()):
                tk.Label(
                    result_grid,
                    text=f"{label}:",
                    font=("Helvetica", 12, "bold"),
                    bg="#f0f8ff"
                ).grid(row=i, column=0, padx=5, pady=2, sticky="e")

                tk.Label(
                    result_grid,
                    text=f"{value}",
                    font=("Helvetica", 12),
                    bg="#f0f8ff"
                ).grid(row=i, column=1, padx=5, pady=2, sticky="w")

            # Create visualization
            self.create_conversion_chart(results)

        except ConversionError as e:
            messagebox.showerror("Conversion Error", str(e))
        # except Exception as e:
        #     # messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def create_conversion_chart(self, results):
        chart_frame = tk.Frame(self.output_frame, bg="#f0f8ff")
        chart_frame.pack(pady=20)

        fig = Figure(figsize=(6, 3), dpi=80, facecolor="#f0f8ff")
        ax = fig.add_subplot(111)

        labels = list(results.keys())
        values = [float(str(v)) for v in results.values()]

        # Normalize values for better visualization
        max_val = max(values)
        normalized = [v / max_val * 100 for v in values] if max_val > 0 else values

        bars = ax.bar(labels, normalized, color=["#4b0082", "#9370db", "#ffa500"])

        ax.set_ylim(0, 110)
        ax.set_ylabel('Normalized Value (%)')
        ax.set_title('Grade Comparison', fontsize=10)
        ax.set_facecolor("#f0f8ff")

        # Add value labels
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{value:.2f}', ha='center', va='bottom')

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # In app/views/calculators/converter.py
    def setup_info_section(self):
        info_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=1, relief="solid")
        info_frame.pack(fill="x", pady=20, padx=10)

        # Title
        tk.Label(
            info_frame,
            text="Grade Conversion Reference",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#4b0082"
        ).pack(anchor="w", padx=15, pady=(10, 5))

        # Create a frame for the table
        table_frame = tk.Frame(info_frame, bg="#ffffff")
        table_frame.pack(fill="x", padx=15, pady=(0, 10))

        # Table headers
        headers = ["Letter", "GPA", "Percentage"]
        for col, header in enumerate(headers):
            tk.Label(
                table_frame,
                text=header,
                font=("Helvetica", 11, "bold"),
                bg="#ffffff",
                fg="#4b0082",
                borderwidth=1,
                relief="solid",
                padx=10,
                pady=5
            ).grid(row=0, column=col, sticky="nsew")

        # Table data
        grade_data = [
            ("A+", "4.0", "97-100%"),
            ("A", "4.0", "93-96%"),
            ("A-", "3.7", "90-92%"),
            ("B+", "3.3", "87-89%"),
            ("B", "3.0", "83-86%"),
            ("B-", "2.7", "80-82%"),
            ("C+", "2.3", "77-79%"),
            ("C", "2.0", "73-76%"),
            ("C-", "1.7", "70-72%"),
            ("D+", "1.3", "67-69%"),
            ("D", "1.0", "65-66%"),
            ("F", "0.0", "Below 65%")
        ]

        for row, (letter, gpa, pct) in enumerate(grade_data, start=1):
            # Letter grade column
            tk.Label(
                table_frame,
                text=letter,
                font=("Helvetica", 10),
                bg="#ffffff",
                borderwidth=1,
                relief="solid",
                padx=10,
                pady=5
            ).grid(row=row, column=0, sticky="nsew")

            # GPA column
            tk.Label(
                table_frame,
                text=gpa,
                font=("Helvetica", 10),
                bg="#ffffff",
                borderwidth=1,
                relief="solid",
                padx=10,
                pady=5
            ).grid(row=row, column=1, sticky="nsew")

            # Percentage column
            tk.Label(
                table_frame,
                text=pct,
                font=("Helvetica", 10),
                bg="#ffffff",
                borderwidth=1,
                relief="solid",
                padx=10,
                pady=5
            ).grid(row=row, column=2, sticky="nsew")

        # Configure grid weights for proper resizing
        for i in range(3):
            table_frame.grid_columnconfigure(i, weight=1)

        # Notes section
        notes_frame = tk.Frame(info_frame, bg="#ffffff")
        notes_frame.pack(fill="x", padx=15, pady=(0, 10))

        tk.Label(
            notes_frame,
            text="Notes:",
            font=("Helvetica", 11, "bold"),
            bg="#ffffff",
            fg="#4b0082"
        ).pack(anchor="w")

        notes = [
            "• These are general guidelines - your institution may use different scales",
            "• Some schools use A+ as 4.3 instead of 4.0",
            "• Percentage ranges may vary by ±2% at different institutions",
            "• Always check your school's specific grading policy"
        ]

        for note in notes:
            tk.Label(
                notes_frame,
                text=note,
                font=("Helvetica", 10),
                bg="#ffffff",
                fg="#333333",
                justify="left"
            ).pack(anchor="w", padx=5, pady=2)