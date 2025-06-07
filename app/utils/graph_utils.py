from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def create_sgpa_chart(parent, grade_points: list, sgpa: float) -> FigureCanvasTkAgg:
    """
    Create and return a matplotlib chart for SGPA visualization
    """
    fig = Figure(figsize=(6, 4), dpi=50, facecolor="#f0f8ff")
    ax = fig.add_subplot(111)

    # Prepare data
    subjects = [f"Subj {i + 1}" for i in range(len(grade_points))]
    points = [gp for _, gp in grade_points]

    # Create bar chart
    bars = ax.bar(subjects, points, color="#9370db")

    # Add SGPA reference line
    ax.axhline(y=sgpa, color="#ffa500", linestyle="--", linewidth=2)
    ax.text(len(subjects) - 0.5, sgpa + 0.1, f'SGPA: {sgpa:.2f}', color="#ffa500")

    # Customize chart
    ax.set_ylim(0, 4.0)
    ax.set_ylabel('Grade Points')
    ax.set_title('Subject Performance')
    ax.set_facecolor("#f0f8ff")
    fig.tight_layout()

    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas