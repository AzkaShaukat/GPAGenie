import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from app.utils.style import configure_styles


class PercentageCalculator:
    def __init__(self, parent_frame, user):
        self.parent = parent_frame
        self.user = user

        # Main container with centered content
        self.main_frame = tk.Frame(parent_frame, bg="#f0f8ff")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Label(
            self.main_frame,
            text="Percentage Calculator",
            font=("Helvetica", 20, "bold"),
            bg="#f0f8ff",
            fg="#4b0082"
        )
        header.pack(pady=(0, 20))

        # Calculator area
        calc_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        calc_frame.pack(expand=True)

        # Input frame (centered)
        input_container = tk.Frame(calc_frame, bg="#f0f8ff")
        input_container.pack()

        # Marks input
        tk.Label(
            input_container,
            text="Obtained Marks:",
            font=("Helvetica", 12),
            bg="#f0f8ff"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.obtained_var = tk.DoubleVar()
        ttk.Entry(
            input_container,
            textvariable=self.obtained_var,
            font=("Helvetica", 12),
            width=20,
            validate="key",
            validatecommand=(self.parent.register(self.validate_number), '%P')
        ).grid(row=0, column=1, padx=10, pady=10)

        # Total marks input
        tk.Label(
            input_container,
            text="Total Marks:",
            font=("Helvetica", 12),
            bg="#f0f8ff"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.total_var = tk.DoubleVar(value=100)
        ttk.Entry(
            input_container,
            textvariable=self.total_var,
            font=("Helvetica", 12),
            width=20,
            validate="key",
            validatecommand=(self.parent.register(self.validate_number), '%P')
        ).grid(row=1, column=1, padx=10, pady=10)

        # Calculate button
        btn_frame = tk.Frame(calc_frame, bg="#f0f8ff")
        btn_frame.pack(pady=20)

        ttk.Button(
            btn_frame,
            text="Calculate Percentage",
            command=self.calculate_percentage,
            style="Accent.TButton"
        ).pack()

        # Results area
        self.results_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        self.results_frame.pack(expand=True, fill="both", pady=10)

        # Info section
        info_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=1, relief="solid")
        info_frame.pack(fill="x", pady=20, padx=10)

        sections = [
            ("How Percentage is Calculated",
             "To calculate your percentage you first must know your total and obtained marks. Then your percentage would be \n"
             "calculated by following formulae:\n\n"
             "                       Percentage = (Obtained Marks ÷ Total Marks) × 100\n\n"
             "\n"
             "Example: If you scored 75 out of 100:\n"
             "(75 ÷ 100) × 100 = 75%"),

            ("Grading Information",
             "Common grading scales:\n"
             "• 90-100%: Excellent (A)\n"
             "• 80-89%: Very Good (B)\n"
             "• 70-79%: Good (C)\n"
             "• 60-69%: Satisfactory (D)\n"
             "• Below 60%: Needs Improvement (F)")
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
                justify="left"
            ).pack(anchor="w", pady=5)

    def validate_number(self, value):
        """Validate that input is a positive number"""
        if not value:
            return True
        try:
            num = float(value)
            return num >= 0
        except ValueError:
            return False

    def calculate_percentage(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        try:
            obtained = self.obtained_var.get()
            total = self.total_var.get()

            if total == 0:
                raise ValueError("Total marks cannot be zero")

            percentage = (obtained / total) * 100

            # Results display
            result_frame = tk.Frame(self.results_frame, bg="#f0f8ff")
            result_frame.pack(expand=True)

            tk.Label(
                result_frame,
                text=f"Your Percentage: {percentage:.2f}%",
                font=("Helvetica", 16, "bold"),
                bg="#f0f8ff",
                fg="#4b0082"
            ).pack(pady=10)

            # Create circular progress chart
            self.create_progress_chart(result_frame, percentage)

        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error: {str(e)}")

    def create_progress_chart(self, parent, percentage):
        fig = Figure(figsize=(4, 4), dpi=80, facecolor="#f0f8ff")
        ax = fig.add_subplot(111)

        # Create donut chart
        achieved = min(percentage, 100)
        remaining = max(0, 100 - achieved)
        sizes = [achieved, remaining]
        colors = ['#4b0082', '#e6e6fa']

        wedges, texts, autotexts = ax.pie(
            sizes,
            colors=colors,
            startangle=90,
            wedgeprops=dict(width=0.3, edgecolor='white'),
            autopct=lambda p: f'{p:.1f}%',
            pctdistance=0.85
        )

        # Center text
        ax.text(0, 0, f"{percentage:.1f}%",
                ha='center', va='center',
                fontsize=24, fontweight='bold',
                color="#4b0082")

        ax.set_title("Percentage Achieved", fontsize=12, pad=20)
        ax.axis('equal')  # Ensure pie is drawn as circle

        fig.tight_layout()

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack()