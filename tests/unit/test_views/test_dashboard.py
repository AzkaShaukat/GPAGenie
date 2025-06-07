import pytest
from unittest.mock import MagicMock
from app.views.dashboard import DashboardWindow
import tkinter as tk


class TestDashboard:
    @pytest.fixture
    def dashboard(self):
        root = tk.Tk()
        user = MagicMock()
        user.role = "regular"
        user.username = "testuser"
        auth_service = MagicMock()
        dashboard = DashboardWindow(root, user, auth_service)
        yield dashboard
        root.destroy()

    def test_initial_setup(self, dashboard):
        assert dashboard.user.username == "testuser"
        assert dashboard.current_view is not None

    def test_navigation(self, dashboard):
        # Test switching views
        dashboard.show_sgpa()
        assert isinstance(dashboard.current_view, MagicMock)  # Would be SGPACalculator in real test

        dashboard.show_cgpa()
        assert isinstance(dashboard.current_view, MagicMock)  # Would be CGPACalculator in real test

        dashboard.show_home()
        assert dashboard.content_frame.winfo_children()

    def test_admin_features(self):
        root = tk.Tk()
        user = MagicMock()
        user.role = "admin"
        auth_service = MagicMock()
        dashboard = DashboardWindow(root, user, auth_service)

        # Check if admin button exists
        admin_buttons = [child for child in dashboard.main_frame.winfo_children()
                         if isinstance(child, tk.Frame) and "Manage Blogs" in str(child.winfo_children())]
        assert len(admin_buttons) > 0
        root.destroy()