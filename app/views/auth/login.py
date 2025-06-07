import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import configure_styles
from app.utils.exceptions import AuthenticationError

class LoginWindow:
    def __init__(self, root, auth_service, on_success_callback):
        self.root = root
        self.auth_service = auth_service
        self.on_success = on_success_callback

        # Center the window on screen and set minimum size
        self.center_window(850, 600)  # Width 800 x Height 600
        self.setup_ui()

    def center_window(self, width, height):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(800, 500)
        # Also configure grid weight for proper resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    def setup_ui(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.main_frame.pack(expand=True, fill="both", padx=50, pady=50)

        # Header
        header = tk.Label(
            self.main_frame,
            text="Welcome to GPAGenie",
            font=("Helvetica", 24, "bold"),
            bg="#f0f8ff",
            fg="#4b0082"
        )
        header.pack(pady=(0, 30))

        # Form container
        form_container = tk.Frame(self.main_frame, bg="#f0f8ff")
        form_container.pack()

        # Username
        tk.Label(form_container, text="Username:", bg="#f0f8ff", font=("Helvetica", 12), anchor="e", width=15) \
            .grid(row=0, column=0, padx=5, pady=2, sticky="e")

        self.username_entry = ttk.Entry(form_container, font=("Helvetica", 12), width=25)
        self.username_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        self.username_error = tk.Label(form_container, text="", fg="red", bg="#f0f8ff", font=("Helvetica", 10))
        self.username_error.grid(row=1, column=1, columnspan=2, padx=5, pady=(0, 8), sticky="w")

        # Password
        tk.Label(form_container, text="Password:", bg="#f0f8ff", font=("Helvetica", 12), anchor="e", width=15) \
            .grid(row=2, column=0, padx=5, pady=2, sticky="e")

        self.password_entry = ttk.Entry(form_container, font=("Helvetica", 12), width=25, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        self.password_error = tk.Label(form_container, text="", fg="red", bg="#f0f8ff", font=("Helvetica", 10))
        self.password_error.grid(row=3, column=1, columnspan=2, padx=5, pady=(0, 8), sticky="w")

        # Button frame
        button_frame = tk.Frame(form_container, bg="#f0f8ff")
        button_frame.grid(row=4, column=1, pady=15, sticky="e")

        login_btn = ttk.Button(
            button_frame,
            text="Login",
            command=self.handle_login,
            style="Accent.TButton"
        )
        login_btn.pack(side="right")

        # Signup link
        signup_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        signup_frame.pack(pady=10)

        tk.Label(
            signup_frame,
            text="Don't have an account?",
            bg="#f0f8ff",
            font=("Helvetica", 10)
        ).pack(side="left")

        signup_link = tk.Label(
            signup_frame,
            text="Sign up",
            fg="#4b0082",
            bg="#f0f8ff",
            font=("Helvetica", 10, "underline"),
            cursor="hand2"
        )
        signup_link.pack(side="left")
        signup_link.bind("<Button-1>", lambda e: self.show_signup())

    def clear_errors(self):
        self.username_error.config(text="")
        self.password_error.config(text="")

    def handle_login(self):
        self.clear_errors()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username:
            self.username_error.config(text="Username is required")
            return
        if not password:
            self.password_error.config(text="Password is required")
            return

        try:
            user = self.auth_service.login(username, password)
            self.on_success(user)
        except AuthenticationError as e:
            self.password_error.config(text=str(e))

    def show_signup(self):
        from app.views.auth.signup import SignupWindow
        SignupWindow(self.root, self.auth_service, self.on_success)