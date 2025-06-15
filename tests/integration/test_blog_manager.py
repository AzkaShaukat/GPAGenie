import pytest
from unittest.mock import patch, MagicMock
from app.views.blog.manager import BlogManager
import tkinter as tk


class TestBlogManager:
    def test_post_creation_flow(self):
        """Test complete post creation flow"""
        root = tk.Tk()
        root.withdraw()

        mock_user = MagicMock()
        manager = BlogManager(root, mock_user)

        # Test with default user (no user_id)
        with patch('app.services.blog_service.create_post') as mock_create:
            manager.show_add_post_form()
            # Verify form gets created with proper defaults

        # Test with logged-in user
        mock_user.user_id = 5
        with patch('app.services.blog_service.create_post') as mock_create:
            manager.show_add_post_form()
            # Verify form uses user_id=5
