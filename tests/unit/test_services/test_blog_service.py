import pytest
from unittest.mock import patch, MagicMock
from app.services.blog_service import create_post, update_post, delete_post, get_all_posts
from app.utils.exceptions import BlogError


class TestBlogService:
    @patch('mysql.connector.connect')
    def test_create_post_requires_author(self, mock_connect):
        """Test that posts require an author_id"""
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        post_data = {
            'title': 'Test Post',
            'excerpt': 'Test excerpt',
            'content': 'Test content'
            # No author_id provided
        }

        with pytest.raises(BlogError) as excinfo:
            create_post(post_data)
        assert "Author ID is required" in str(excinfo.value)

    @patch('mysql.connector.connect')
    def test_create_post_with_valid_author(self, mock_connect):
        """Test successful post creation with valid author"""
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'user_id': 2}  # Simulate author exists

        post_data = {
            'title': 'Test Post',
            'excerpt': 'Test excerpt',
            'content': 'Test content',
            'author_id': 2
        }

        create_post(post_data)

        # Verify the SQL executed with correct author_id
        mock_cursor.execute.assert_called()
        args, _ = mock_cursor.execute.call_args_list[1]  # Second call is the INSERT
        assert args[1][4] == 2  # author_id position in VALUES tuple

    @patch('mysql.connector.connect')
    def test_create_post_with_invalid_author(self, mock_connect):
        """Test error when author doesn't exist"""
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # Simulate author doesn't exist

        post_data = {
            'title': 'Test Post',
            'author_id': 999,  # Non-existent author
            'excerpt': 'Test',
            'content': 'Test'
        }

        with pytest.raises(BlogError) as excinfo:
            create_post(post_data)
        assert "does not exist in the users table" in str(excinfo.value)
