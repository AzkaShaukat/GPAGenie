import tkinter as tk
from tkinter import messagebox
from app.views.auth.login import LoginWindow
from app.utils.style import configure_styles
from app.services.auth import AuthService
import mysql.connector


class GPAGenieApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GPAGenie - Academic Performance Tracker")
        self.root.geometry("900x600")

        # Configure styles
        configure_styles()

        # Initialize database connection
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="gpa_genie1"
            )
            self.auth_service = AuthService(self.db_connection)

            # Start with login window
            LoginWindow(self.root, self.auth_service, self.show_dashboard)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Cannot connect to database: {err}")
            self.root.destroy()

    def show_dashboard(self, user):
        """Callback after successful login to show main dashboard"""
        from app.views.dashboard import DashboardWindow
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        # Show dashboard
        DashboardWindow(self.root, user, self.auth_service)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GPAGenieApp()
    app.run()