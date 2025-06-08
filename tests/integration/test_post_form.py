import pytest
from unittest.mock import patch, MagicMock
from app.views.blog.post_form import BlogPostForm
import tkinter as tk


class TestBlogPostForm:
    def test_submit_form_default_author(self):
        """Test form submission uses default author_id=1"""
        root = tk.Tk()
        root.withdraw()

        mock_user = MagicMock()
        mock_blog_manager = MagicMock()

        form = BlogPostForm(root, mock_user, mock_blog_manager, mode="create")

        # Simulate form inputs
        form.title_entry.insert(0, "Test Title")
        form.content_text.insert("1.0", "Test Content")

        with patch('app.services.blog_service.create_post') as mock_create:
            form.submit_form()

            # Verify create_post called with author_id=1
            args, kwargs = mock_create.call_args
            assert args[0]['author_id'] == 1

    def test_submit_form_validation(self):
        """Test required field validation"""
        root = tk.Tk()
        root.withdraw()

        form = BlogPostForm(root, MagicMock(), MagicMock(), mode="create")

        # Don't fill any fields
        with patch('tkinter.messagebox.showerror') as mock_error:
            form.submit_form()
            mock_error.assert_called()  # Should show error

        # Verify error labels
        assert "required" in form.error_labels['title'].cget("text")
        assert "required" in form.error_labels['content'].cget("text")