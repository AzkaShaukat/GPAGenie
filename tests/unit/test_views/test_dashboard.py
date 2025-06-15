import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch, call
from app.views.dashboard import DashboardWindow


class TestDashboard:
    @pytest.fixture
    def dashboard(self):
        # Use TclError workaround for tests
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the window during tests
        except tk.TclError:
            root = tk.Tk()  # Try again if first attempt fails

        user = MagicMock()
        user.username = "testuser"
        user.role = "student"
        user.full_name = "Test User"
        auth_service = MagicMock()
        dashboard = DashboardWindow(root, user, auth_service)
        yield dashboard
        root.destroy()

    def test_initial_setup(self, dashboard):
        assert dashboard.user.username == "testuser"
        # Home view doesn't set current_view, so we shouldn't expect it
        assert dashboard.current_view is None

    @patch('app.views.dashboard.SGPACalculator')
    def test_navigation(self, mock_sgpa, dashboard):
        # Test switching views
        dashboard.show_sgpa()

        # Verify SGPACalculator was instantiated with correct arguments
        mock_sgpa.assert_called_once_with(dashboard.content_frame, dashboard.user)
        assert dashboard.current_view == mock_sgpa.return_value
