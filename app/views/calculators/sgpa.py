# sgpa.py

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from app.services.calculations import calculate_sgpa
from app.utils.style import configure_styles


class SGPACalculator:
    def __init__(self, parent_frame, user):
        self.parent = parent_frame
        self.user = user
        self.subjects = []
        self.setup_ui()

    def setup_ui(self):
        # This main_frame holds all calculator content and is centered by its parent
        main_frame = tk.Frame(self.parent, bg="#f0f8ff")
        main_frame.pack(expand=True, padx=20, pady=20)

        header = tk.Label(
            main_frame, text="SGPA Calculator", font=("Helvetica", 20, "bold"),
            bg="#f0f8ff", fg="#4b0082"
        )
        header.pack(pady=(0, 20))

        calc_frame = tk.Frame(main_frame, bg="#f0f8ff")
        calc_frame.pack(fill="x", pady=10)

        entry_container = tk.Frame(calc_frame, bg="#f0f8ff")
        entry_container.pack()

        self.entry_frame = tk.Frame(entry_container, bg="#f0f8ff")
        self.entry_frame.pack()

        headers = ["Subject (Optional)", "Grade", "Credit Hours"]
        for col, text in enumerate(headers):
            tk.Label(
                self.entry_frame, text=text, font=("Helvetica", 12, "bold"),
                bg="#f0f8ff", fg="#4b0082"
            ).grid(row=0, column=col, padx=10, pady=5)

        self.add_subject_row()
        self.add_subject_row()
        self.add_subject_row()

        btn_container = tk.Frame(calc_frame, bg="#f0f8ff")
        btn_container.pack()
        btn_frame = tk.Frame(btn_container, bg="#f0f8ff")
        btn_frame.pack(fill="x", pady=20)

        add_btn = ttk.Button(
            btn_frame, text="+ Add Subject", command=self.add_subject_row, style="Accent.TButton"
        )
        add_btn.pack(side="left", padx=5)

        calculate_btn = ttk.Button(
            btn_frame, text="Calculate SGPA", command=self.calculate_sgpa, style="Accent.TButton"
        )
        calculate_btn.pack(side="left", padx=5)

        self.results_frame = tk.Frame(main_frame, bg="#f0f8ff")
        self.results_frame.pack(fill="x", pady=10)

        # --- Informational Sections ---
        info_wrapper = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
        info_wrapper.pack(fill="x", pady=20, padx=10)

        # How it's Calculated
        info_frame1 = tk.Frame(info_wrapper, bg="#ffffff")
        info_frame1.pack(fill="x", pady=10, padx=15)

        tk.Label(
            info_frame1, text="How SGPA is Calculated", font=("Helvetica", 14, "bold"),
            bg="#ffffff", fg="#4b0082"
        ).pack(anchor="w")

        info_text1 = "Your Semester Grade Point Average (SGPA) is calculated by multiplying the grade points of each course by its credit hours, summing the results, and then dividing by the total credit hours for the semester. It's a precise reflection of your performance in a given term."
        tk.Label(
            info_frame1, text=info_text1, font=("Helvetica", 11),
            bg="#ffffff", fg="#333333", justify="left", wraplength=700
        ).pack(anchor="w", pady=5)

        # Why it's Important
        info_frame2 = tk.Frame(info_wrapper, bg="#ffffff")
        info_frame2.pack(fill="x", pady=10, padx=15)

        tk.Label(
            info_frame2, text="Why Your SGPA Matters", font=("Helvetica", 14, "bold"),
            bg="#ffffff", fg="#4b0082"
        ).pack(anchor="w")

        info_text2 = "A strong SGPA is crucial for maintaining good academic standing, qualifying for scholarships, and being eligible for dean's lists or honor rolls. It's also a key factor in applications for internships, graduate school, and future job opportunities. Consistently monitoring your SGPA helps you stay on track toward your long-term academic and career goals."
        tk.Label(
            info_frame2, text=info_text2, font=("Helvetica", 11),
            bg="#ffffff", fg="#333333", justify="left", wraplength=700
        ).pack(anchor="w", pady=5)

    def add_subject_row(self):
        row = len(self.subjects) + 1
        subject_var = tk.StringVar()
        subject_entry = ttk.Entry(self.entry_frame, textvariable=subject_var, font=("Helvetica", 11), width=20)
        subject_entry.grid(row=row, column=0, padx=10, pady=5)

        grade_var = tk.StringVar()
        grade_choices = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]
        grade_dropdown = ttk.Combobox(self.entry_frame, textvariable=grade_var, values=grade_choices,
                                      font=("Helvetica", 11), width=5, state="readonly")
        grade_dropdown.grid(row=row, column=1, padx=10, pady=5)
        grade_dropdown.set("A")

        credit_var = tk.IntVar(value=3)
        credit_dropdown = ttk.Combobox(self.entry_frame, textvariable=credit_var, values=[1, 2, 3, 4, 5],
                                       font=("Helvetica", 11), width=3, state="readonly")
        credit_dropdown.grid(row=row, column=2, padx=10, pady=5)

        self.subjects.append({"subject": subject_var, "grade": grade_var, "credits": credit_var})

    def calculate_sgpa(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        subjects_data = []
        for i, sub in enumerate(self.subjects):
            grade, credits = sub["grade"].get(), sub["credits"].get()
            if not grade:
                messagebox.showerror("Input Error", f"Please select a grade for all subjects.")
                return
            subjects_data.append(
                {"subject": sub["subject"].get() or f"Subject {i + 1}", "grade": grade, "credits": credits})

        try:
            sgpa, grade_points = calculate_sgpa(subjects_data)

            result_frame = tk.Frame(self.results_frame, bg="#f0f8ff")
            result_frame.pack(pady=10)
            tk.Label(result_frame, text=f"Your SGPA is: {sgpa:.2f}", font=("Helvetica", 16, "bold"), bg="#f0f8ff",
                     fg="#4b0082").pack(pady=10)

            details_frame = tk.Frame(self.results_frame, bg="#f0f8ff")
            details_frame.pack(pady=10, fill="x", expand=True)

            table_frame = tk.Frame(details_frame, bg="#f0f8ff")
            table_frame.pack(side="left", padx=20, anchor="n")

            headers = ["Subject", "Grade", "Credits", "Quality Points"]
            for col, header in enumerate(headers):
                tk.Label(table_frame, text=header, font=("Helvetica", 11, "bold"), bg="#f0f8ff", fg="#4b0082").grid(
                    row=0, column=col, padx=10, pady=5)

            for r, (subj, gp) in enumerate(grade_points, start=1):
                tk.Label(table_frame, text=subj["subject"], font=("Helvetica", 11), bg="#f0f8ff").grid(row=r, column=0,
                                                                                                       padx=10, pady=2,
                                                                                                       sticky='w')
                tk.Label(table_frame, text=subj["grade"], font=("Helvetica", 11), bg="#f0f8ff").grid(row=r, column=1,
                                                                                                     padx=10, pady=2)
                tk.Label(table_frame, text=str(subj["credits"]), font=("Helvetica", 11), bg="#f0f8ff").grid(row=r,
                                                                                                            column=2,
                                                                                                            padx=10,
                                                                                                            pady=2)
                tk.Label(table_frame, text=f"{gp:.2f}", font=("Helvetica", 11), bg="#f0f8ff").grid(row=r, column=3,
                                                                                                   padx=10, pady=2)

            chart_frame = tk.Frame(details_frame, bg="#f0f8ff")
            chart_frame.pack(side="left", expand=True, padx=20)
            self.create_circular_progress(chart_frame, sgpa)

        except Exception as e:
            messagebox.showerror("Calculation Error", f"An unexpected error occurred: {e}")

    def create_circular_progress(self, container, sgpa):
        # MODIFIED: Changed figsize for a more compact graph and used tight_layout.
        fig = Figure(figsize=(2.5, 2.5), dpi=100, facecolor="#f0f8ff")
        ax = fig.add_subplot(111)

        values = [sgpa, max(0, 4.0 - sgpa)]
        colors = ['#4b0082', '#e6e6fa']

        ax.pie(values, wedgeprops=dict(width=0.2), startangle=90, colors=colors)
        ax.text(0, 0, f"{sgpa:.2f}", ha='center', va='center', fontsize=20, fontweight='bold', color="#4b0082")
        ax.set_title("SGPA on 4.0 Scale", fontsize=9, pad=5, color="#333333")

        # MODIFIED: Use tight_layout to reduce padding within the figure.
        fig.tight_layout(pad=0)

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=5)