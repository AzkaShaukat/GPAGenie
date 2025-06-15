import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import configure_styles
from app.utils.exceptions import RegistrationError

class SignupWindow:
    def __init__(self, parent_frame, auth_service, on_success_callback):
        self.parent = parent_frame
        self.auth_service = auth_service
        self.on_success = on_success_callback

        # Center the window on screen and set minimum size
        self.center_window(850, 700)  # Width 800 x Height 600
        self.setup_ui()

    def center_window(self, width, height):
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.parent.geometry(f"{width}x{height}+{x}+{y}")
        self.parent.minsize(800, 500)
        # Also configure grid weight for proper resizing
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

    def setup_ui(self):
        # Clear any existing widgets
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Main container frame
        self.main_frame = tk.Frame(self.parent, bg="#f0f8ff")
        self.main_frame.pack(expand=True, fill="both", padx=50, pady=50)

        # Header
        header = tk.Label(
            self.main_frame,
            text="Create New Account",
            font=("Helvetica", 20, "bold"),
            bg="#f0f8ff",
            fg="#4b0082"
        )
        header.pack(pady=(0, 20))

        # Form container
        form_container = tk.Frame(self.main_frame, bg="#f0f8ff")
        form_container.pack()

        # Form fields with labels and entries
        fields = [
            ("Full Name:", "name"),
            ("Username:", "username"),
            ("Email:", "email"),
            ("Password:", "password"),
            ("Confirm Password:", "confirm_password")
        ]

        self.entries = {}
        self.error_labels = {}

        for i, (label_text, field_name) in enumerate(fields):
            label = tk.Label(form_container, text=label_text, bg="#f0f8ff", font=("Helvetica", 12), anchor="e",
                             width=15)
            label.grid(row=i * 2, column=0, padx=5, pady=2, sticky="e")

            entry = ttk.Entry(form_container, font=("Helvetica", 12), width=25,
                              show="*" if "password" in field_name else "")
            entry.grid(row=i * 2, column=1, padx=5, pady=2, sticky="w")
            self.entries[field_name] = entry

            error_label = tk.Label(form_container, text="", fg="red", bg="#f0f8ff", font=("Helvetica", 10),
                                   wraplength=200)
            error_label.grid(row=i * 2 + 1, column=1, columnspan=2, padx=5, pady=(0, 8), sticky="w")
            self.error_labels[field_name] = error_label

        # Add admin registration checkbox (visible only if no admin exists)
        self.is_admin_var = tk.BooleanVar(value=False)
        if not self.auth_service.admin_exists():
            admin_check = ttk.Checkbutton(
                form_container,
                text="Register as Administrator",
                variable=self.is_admin_var,
                style="TCheckbutton"
            )
            admin_check.grid(row=len(fields) * 2, columnspan=2, pady=5)

        # Password requirements
        requirements = tk.Label(
            form_container,
            text="Password must contain:\n- 8+ characters\n- 1 uppercase letter\n- 1 digit",
            bg="#f0f8ff",
            fg="#666666",
            font=("Helvetica", 9),
            justify="left"
        )
        requirements.grid(row=len(fields) * 2 + 1, column=1, pady=(0, 10), sticky="w")

        # Button frame
        button_frame = tk.Frame(form_container, bg="#f0f8ff")
        button_frame.grid(row=len(fields) * 2 + 2, column=1, pady=15, sticky="e")

        signup_btn = ttk.Button(
            button_frame,
            text="Sign Up",
            command=self.handle_signup,
            style="Accent.TButton"
        )
        signup_btn.pack(side="right")

        # Login link (already have an account)
        login_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        login_frame.pack(pady=10)

        tk.Label(
            login_frame,
            text="Already have an account?",
            bg="#f0f8ff",
            font=("Helvetica", 10)
        ).pack(side="left")

        login_link = tk.Label(
            login_frame,
            text="Login",
            fg="#4b0082",
            bg="#f0f8ff",
            font=("Helvetica", 10, "underline"),
            cursor="hand2"
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.show_login())

    def clear_errors(self):
        for label in self.error_labels.values():
            label.config(text="")

    def handle_signup(self):
        self.clear_errors()

        full_name = self.entries['name'].get()
        username = self.entries['username'].get()
        email = self.entries['email'].get()
        password = self.entries['password'].get()
        confirm_password = self.entries['confirm_password'].get()
        is_admin = getattr(self, 'is_admin_var', False) and self.is_admin_var.get()

        # Validate password match
        if password != confirm_password:
            self.error_labels['confirm_password'].config(text="Passwords do not match")
            return

        try:
            user = self.auth_service.register(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                is_admin=is_admin
            )
            role_msg = "Admin " if is_admin else ""
            messagebox.showinfo("Success", f"{role_msg}Account created successfully!")
            self.on_success(user)
        except Exception as e:
            error_msg = str(e)
            if "Username must be" in error_msg:
                self.error_labels['username'].config(text=error_msg)
            elif "Invalid email" in error_msg:
                self.error_labels['email'].config(text=error_msg)
            elif "Password must" in error_msg:
                self.error_labels['password'].config(text=error_msg)
            elif "already exists" in error_msg.lower():
                if "username" in error_msg.lower():
                    self.error_labels['username'].config(text=error_msg)
                else:
                    self.error_labels['email'].config(text=error_msg)
            else:
                messagebox.showerror("Error", error_msg)

    def show_login(self):
        from app.views.auth.login import LoginWindow
        LoginWindow(self.parent, self.auth_service, self.on_success)