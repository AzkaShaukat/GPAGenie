import tkinter as tk
from tkinter import ttk


def configure_styles():
    style = ttk.Style()

    # Configure main styles
    style.theme_use('clam')

    # Colors
    primary_color = "#4b0082"  # Indigo
    secondary_color = "#9370db"  # Medium purple
    accent_color = "#ffa500"  # Orange
    background_color = "#f0f8ff"  # Alice blue
    text_color = "#333333"

    # Configure main frame style
    style.configure(
        'TFrame',
        background=background_color
    )

    # Configure label style
    style.configure(
        'TLabel',
        background=background_color,
        foreground=text_color,
        font=('Helvetica', 10)
    )

    # Configure entry style
    style.configure(
        'TEntry',
        fieldbackground='white',
        foreground=text_color,
        font=('Helvetica', 10),
        padding=5,
        bordercolor=secondary_color,
        lightcolor=secondary_color,
        darkcolor=secondary_color
    )

    # Configure button styles
    style.configure(
        'TButton',
        font=('Helvetica', 10, 'bold'),
        background=secondary_color,
        foreground='white',
        padding=10,
        borderwidth=0
    )

    style.map(
        'TButton',
        background=[('active', primary_color), ('disabled', '#cccccc')],
        foreground=[('disabled', '#666666')]
    )

    # Accent button style
    style.configure(
        'Accent.TButton',
        background=accent_color,
        foreground='white'
    )

    style.map(
        'Accent.TButton',
        background=[('active', '#ff8c00'), ('disabled', '#cccccc')]
    )