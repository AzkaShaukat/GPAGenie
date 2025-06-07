# dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox
from app.views.calculators.sgpa import SGPACalculator
# Note: The following imports are placeholders. You will need to create and
# import these classes for the corresponding features to work.
from app.views.calculators.cgpa import CGPACalculator
from app.views.calculators.percentage import PercentageCalculator
from app.views.calculators.converter import GradeConverter
# from app.views.blog.viewer import BlogViewer
# from app.views.blog.manager import BlogManager
# from app.views.about import AboutSection
from app.utils.style import configure_styles


class DashboardWindow:
    def __init__(self, parent, user, auth_service):
        self.parent = parent
        self.user = user
        self.auth_service = auth_service
        self.current_view = None

        # Center the window on screen and set minimum size
        self.center_window(850, 600)  # Width 800 x Height 600
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
        # Clear any existing widgets from the root window
        for widget in self.parent.winfo_children():
            widget.destroy()

        # The main frame that holds the header and the scrollable content area
        self.main_container = tk.Frame(self.parent)
        self.main_container.pack(expand=True, fill="both")

        # --- Header Bar (Consistent Across All Views) ---
        self.setup_header()


        # --- Scrollable Content Area ---
        content_area = tk.Frame(self.main_container)
        content_area.pack(expand=True, fill="both")

        self.canvas = tk.Canvas(content_area, bg="#f0f8ff", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(content_area, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f8ff")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        # --- Centering Layout ---
        # This container uses a grid to center the content_frame within the scrollable area.
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # This is the frame where views (Home, SGPA, etc.) will be placed.
        # Its content will be centered due to the parent's grid configuration.
        self.content_frame = tk.Frame(self.scrollable_frame, bg="#f0f8ff")
        # MODIFIED: Removed sticky="nsew" to allow the frame to center itself instead of stretching.
        self.content_frame.grid(row=0, column=0)

        # Load the initial home view
        self.show_home()

    def _on_mousewheel(self, event):
        # Simplified cross-platform mouse wheel scrolling
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

    def setup_header(self):
        # The header frame is fixed at the top and will not scroll
        header_frame = tk.Frame(self.main_container, bg="#4b0082", height=60)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        left_menu = tk.Frame(header_frame, bg="#4b0082")
        left_menu.pack(side="left", padx=0, pady=5)

        right_menu = tk.Frame(header_frame, bg="#4b0082")
        right_menu.pack(side="right", padx=0, pady=5)

        # MODIFIED: Logic to place "Manage Blogs" tab correctly for admins.
        menu_buttons_data = [
            ("Home", self.show_home),
            ("SGPA", self.show_sgpa),
            ("CGPA", self.show_cgpa),
            ("Prcntg", self.show_percentage),
            ("Cnvrtr", self.show_converter),
            ("Blogs", self.show_blogs),
        ]

        # Conditionally insert "Manage Blogs" for admin users
        if self.user.role == "admin":
            menu_buttons_data.append(("Manage", self.show_blog_manager))

        menu_buttons_data.append(("About", self.show_about))

        for text, command in menu_buttons_data:
            btn = ttk.Button(left_menu, text=text, command=command, style="Header.TButton")
            btn.pack(side="left", padx=0, pady=5)

        # User info and actions on the right side
        logout_btn = ttk.Button(right_menu, text="Logout", command=self.logout, style="Header.TButton")
        logout_btn.pack(side="right", padx=0, pady=5)

        # MODIFIED: Removed the old admin button from the right side.
        user_frame = tk.Frame(right_menu, bg="#4b0082")
        user_frame.pack(side="right", padx=0, pady=5)

        # tk.Label(
        #     user_frame,
        #     text=f"Hi! {self.user.username}",
        #     fg="white", bg="#4b0082", font=("Helvetica", 10)
        # ).pack(side="right")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_view = None
        self.canvas.yview_moveto(0) # Reset scroll to top

    def show_home(self):
        self.clear_content()

        # Wrapper frame to hold all home content, allowing it to be centered as a single block
        home_wrapper = tk.Frame(self.content_frame, bg="#f0f8ff")
        home_wrapper.pack(expand=True, pady=20, padx=50) # Add some padding for better spacing

        welcome_frame = tk.Frame(home_wrapper, bg="#f0f8ff")
        welcome_frame.pack(pady=(20, 10))
        tk.Label(
            welcome_frame, text=f"Welcome to GPAGenie, {self.user.full_name or self.user.username}!",
            font=("Helvetica", 24, "bold"), bg="#f0f8ff", fg="#4b0082"
        ).pack(pady=10)

        desc_frame = tk.Frame(home_wrapper, bg="#f0f8ff")
        desc_frame.pack(fill="x", pady=10, padx=20)

        tk.Label(
            desc_frame,
            text="GPAGenie is your all-in-one academic toolkit, designed to simplify the way you track, calculate, and understand your academic performance. Our goal is to empower you with the tools and information you need to stay on top of your studies and achieve your academic goals.",
            font=("Helvetica", 12), bg="#f0f8ff", fg="#333333", wraplength=700, justify="center"
        ).pack(pady=5)

        tk.Label(
            desc_frame, text="Key Features at a Glance:",
            font=("Helvetica", 12, "bold"), bg="#f0f8ff", fg="#4b0082"
        ).pack(pady=(15, 5))

        features = [
            "• Instantly calculate your SGPA and CGPA with high accuracy.",
            "• Seamlessly convert grades between different systems (e.g., GPA to percentage).",
            "• Visualize your academic progress with intuitive charts and graphs.",
            "• Access insightful blog content to help you improve your study habits and career prospects."
        ]
        for feature in features:
            tk.Label(
                desc_frame, text=feature, font=("Helvetica", 11), bg="#f0f8ff",
                fg="#333333", justify="left"
            ).pack(fill="x", padx=40, anchor="w")

        self.actions_frame = tk.Frame(home_wrapper, bg="#f0f8ff")
        self.actions_frame.pack(pady=30)

        self.get_started_btn = ttk.Button(
            self.actions_frame, text="Get Started", command=self.show_home_options,
            style="Accent.TButton", width=20
        )
        self.get_started_btn.pack()

        self.options_container = tk.Frame(self.actions_frame, bg="#f0f8ff")
        self.options_container.pack(pady=(10, 0))

        quote_frame = tk.Frame(home_wrapper, bg="#f0f8ff")
        quote_frame.pack(pady=40, fill="x")
        tk.Label(
            quote_frame, text='"Success is the sum of small efforts, repeated day in and day out."',
            font=("Helvetica", 14, "italic"), bg="#f0f8ff", fg="#4b0082"
        ).pack()
        tk.Label(
            quote_frame, text="— Robert Collier", font=("Helvetica", 10),
            bg="#f0f8ff", fg="#4b0082"
        ).pack(pady=(5, 0))

    def show_home_options(self):
        self.get_started_btn.pack_forget()
        tk.Label(
            self.options_container, text="Select an option to get started:",
            font=("Helvetica", 14, "bold"), bg="#f0f8ff", fg="#4b0082"
        ).pack(pady=(0, 20))
        options = [
            ("SGPA Calculator", self.show_sgpa), ("CGPA Calculator", self.show_cgpa),
            ("Percentage Calculator", self.show_percentage), ("Grade Converter", self.show_converter),
            ("View Blogs", self.show_blogs),
        ]
        for text, command in options:
            btn = ttk.Button(
                self.options_container, text=text, command=command,
                style="Accent.TButton", width=25
            ).pack(pady=10)

    def show_sgpa(self):
        self.clear_content()
        self.current_view = SGPACalculator(self.content_frame, self.user)

    def show_cgpa(self):
        self.clear_content()
        self.current_view = CGPACalculator(self.content_frame, self.user)


    def show_percentage(self):
        self.clear_content()
        self.current_view = PercentageCalculator(self.content_frame, self.user)

    def show_converter(self):
        self.clear_content()
        self.current_view = GradeConverter(self.content_frame)

    def show_blogs(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Blog Viewer is not implemented yet.", font=("Helvetica", 14),
                 bg="#f0f8ff").pack(expand=True)

    def show_blog_manager(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Blog Manager is not implemented yet.", font=("Helvetica", 14),
                 bg="#f0f8ff").pack(expand=True)

    def show_about(self):
        self.clear_content()
        tk.Label(self.content_frame, text="About section is not implemented yet.", font=("Helvetica", 14),
                 bg="#f0f8ff").pack(expand=True)

    def logout(self):
        from app.views.auth.login import LoginWindow
        if messagebox.askokcancel("Logout", "Are you sure you want to logout?"):
            self.auth_service.logout()
            for widget in self.parent.winfo_children():
                widget.destroy()
            LoginWindow(self.parent, self.auth_service,
                        lambda user: DashboardWindow(self.parent, user, self.auth_service))