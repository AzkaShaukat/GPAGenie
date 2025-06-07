import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from app.services.calculations import calculate_cgpa
from app.utils.style import configure_styles


class CGPACalculator:
    def __init__(self, parent_frame, user):
        self.parent = parent_frame
        self.user = user
        self.semesters = []

        # Main container with centered content
        self.main_frame = tk.Frame(parent_frame, bg="#f0f8ff")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Label(
            self.main_frame,
            text="CGPA Calculator",
            font=("Helvetica", 20, "bold"),
            bg="#f0f8ff",
            fg="#4b0082"
        )
        header.pack(pady=(0, 20))

        # Calculator area
        calc_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        calc_frame.pack(expand=True)

        # Semester entry frame (centered)
        entry_container = tk.Frame(calc_frame, bg="#f0f8ff")
        entry_container.pack()

        self.entry_frame = tk.Frame(entry_container, bg="#f0f8ff")
        self.entry_frame.pack()

        # Column headers
        headers = ["Semester", "SGPA", "Total Credits"]
        for col, text in enumerate(headers):
            tk.Label(
                self.entry_frame,
                text=text,
                font=("Helvetica", 12, "bold"),
                bg="#f0f8ff",
                fg="#4b0082"
            ).grid(row=0, column=col, padx=10, pady=5)

        # Initial rows
        self.add_semester_row()
        self.add_semester_row()

        # Buttons (centered)
        btn_container = tk.Frame(calc_frame, bg="#f0f8ff")
        btn_container.pack(pady=10)

        ttk.Button(
            btn_container,
            text="+ Add Semester",
            command=self.add_semester_row,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_container,
            text="Calculate CGPA",
            command=self.calculate_cgpa,
            style="Accent.TButton"
        ).pack(side="left", padx=5)

        # Results area
        self.results_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        self.results_frame.pack(expand=True, fill="both", pady=10)

        # Info section
        info_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=1, relief="solid")
        info_frame.pack(fill="x", pady=20, padx=10)

        sections = [
            ("How CGPA is Calculated",
             "Multiply each semester's SGPA by its total credits, sum these values, "
             "then divide by the sum of all credits. Example: 3.5 SGPA with 15 credits = 52.5 quality points."),

            ("Why CGPA Matters",
             "CGPA represents your cumulative academic performance. It's crucial for "
             "graduation requirements, honors eligibility, and job applications.")
        ]

        for title, text in sections:
            section_frame = tk.Frame(info_frame, bg="#ffffff")
            section_frame.pack(fill="x", pady=10, padx=15)

            tk.Label(
                section_frame,
                text=title,
                font=("Helvetica", 14, "bold"),
                bg="#ffffff",
                fg="#4b0082"
            ).pack(anchor="w")

            tk.Label(
                section_frame,
                text=text,
                font=("Helvetica", 11),
                bg="#ffffff",
                fg="#333333",
                justify="left",
                wraplength=700
            ).pack(anchor="w", pady=5)

    def add_semester_row(self):
        row = len(self.semesters) + 1

        # Semester name
        name_var = tk.StringVar(value=f"Semester {row}")
        ttk.Entry(
            self.entry_frame,
            textvariable=name_var,
            font=("Helvetica", 11),
            width=15
        ).grid(row=row, column=0, padx=10, pady=5)

        # SGPA entry
        sgpa_var = tk.DoubleVar()
        ttk.Entry(
            self.entry_frame,
            textvariable=sgpa_var,
            font=("Helvetica", 11),
            width=8,
            validate="key",
            validatecommand=(self.parent.register(self.validate_grade), '%P')
        ).grid(row=row, column=1, padx=10, pady=5)

        # Credits entry
        credits_var = tk.IntVar(value=15)
        ttk.Combobox(
            self.entry_frame,
            textvariable=credits_var,
            values=list(range(12, 25)),
            font=("Helvetica", 11),
            width=5,
            state="readonly"
        ).grid(row=row, column=2, padx=10, pady=5)

        self.semesters.append({
            "name": name_var,
            "sgpa": sgpa_var,
            "credits": credits_var
        })

    def validate_grade(self, value):
        try:
            if not value:
                return True
            num = float(value)
            return 0.0 <= num <= 4.0
        except ValueError:
            return False

    def calculate_cgpa(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Prepare data
        semesters_data = []
        for sem in self.semesters:
            if not sem["sgpa"].get():
                messagebox.showerror("Error", "Please enter SGPA for all semesters")
                return

            semesters_data.append({
                "name": sem["name"].get(),
                "sgpa": sem["sgpa"].get(),
                "credits": sem["credits"].get()
            })

        try:
            cgpa, semester_points = calculate_cgpa(semesters_data)

            # Results display
            result_container = tk.Frame(self.results_frame, bg="#f0f8ff")
            result_container.pack(expand=True)

            tk.Label(
                result_container,
                text=f"Your CGPA: {cgpa:.2f}",
                font=("Helvetica", 16, "bold"),
                bg="#f0f8ff",
                fg="#4b0082"
            ).pack(pady=10)

            # Table and chart container
            details_frame = tk.Frame(result_container, bg="#f0f8ff")
            details_frame.pack(expand=True, pady=10)

            # Table
            table_frame = tk.Frame(details_frame, bg="#f0f8ff")
            table_frame.pack(side="left", padx=20, anchor="n")

            headers = ["Semester", "SGPA", "Credits", "Quality Points"]
            for col, text in enumerate(headers):
                tk.Label(
                    table_frame,
                    text=text,
                    font=("Helvetica", 11, "bold"),
                    bg="#f0f8ff",
                    fg="#4b0082"
                ).grid(row=0, column=col, padx=10, pady=5)

            for row, (sem, qp) in enumerate(semester_points, 1):
                tk.Label(
                    table_frame,
                    text=sem["name"],
                    font=("Helvetica", 11),
                    bg="#f0f8ff"
                ).grid(row=row, column=0, padx=10, pady=2, sticky="w")

                tk.Label(
                    table_frame,
                    text=f"{sem['sgpa']:.2f}",
                    font=("Helvetica", 11),
                    bg="#f0f8ff"
                ).grid(row=row, column=1, padx=10, pady=2)

                tk.Label(
                    table_frame,
                    text=str(sem["credits"]),
                    font=("Helvetica", 11),
                    bg="#f0f8ff"
                ).grid(row=row, column=2, padx=10, pady=2)

                tk.Label(
                    table_frame,
                    text=f"{qp:.2f}",
                    font=("Helvetica", 11),
                    bg="#f0f8ff"
                ).grid(row=row, column=3, padx=10, pady=2)

            # Chart
            chart_frame = tk.Frame(details_frame, bg="#f0f8ff")
            chart_frame.pack(side="left", expand=True, padx=20)
            self.create_trend_chart(chart_frame, semesters_data, cgpa)

        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {str(e)}")

    def create_trend_chart(self, container, semesters_data, cgpa):
        # MODIFIED: Changed figsize for a more compact graph and used tight_layout.
        fig = Figure(figsize=(2.5, 2.5), dpi=100, facecolor="#f0f8ff")
        ax = fig.add_subplot(111)

        values = [cgpa, max(0, 4.0 - cgpa)]
        colors = ['#4b0082', '#e6e6fa']

        ax.pie(values, wedgeprops=dict(width=0.2), startangle=90, colors=colors)
        ax.text(0, 0, f"{cgpa:.2f}", ha='center', va='center', fontsize=20, fontweight='bold', color="#4b0082")
        ax.set_title("CGPA on 4.0 Scale", fontsize=9, pad=5, color="#333333")

        # MODIFIED: Use tight_layout to reduce padding within the figure.
        fig.tight_layout(pad=0)

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=5)