import pytest
from unittest.mock import patch, MagicMock
from app.services.blog_service import create_post, update_post, delete_post, get_all_posts
from app.utils.exceptions import BlogError


class TestBlogService:
    @patch('mysql.connector.connect')
    def test_create_post_with_default_author(self, mock_connect):
        """Test that posts are created with author_id=1 by default"""
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        post_data = {
            'title': 'Test Post',
            'excerpt': 'Test excerpt',
            'content': 'Test content'
        }

        create_post(post_data)

        # Verify the SQL executed with author_id=1
        mock_cursor.execute.assert_called_once()
        args, kwargs = mock_cursor.execute.call_args
        assert args[1][4] == 1  # author_id position in VALUES tuple

    @patch('mysql.connector.connect')
    def test_create_post_with_explicit_author(self, mock_connect):
        """Test that explicit author_id overrides default"""
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        post_data = {
            'title': 'Test Post',
            'excerpt': 'Test excerpt',
            'content': 'Test content',
            'author_id': 2  # Explicit author
        }

        create_post(post_data)

        # Verify the SQL uses explicit author_id
        args, kwargs = mock_cursor.execute.call_args
        assert args[1][4] == 2

    @patch('mysql.connector.connect')
    def test_create_post_db_error(self, mock_connect):
        """Test error handling for database failures"""
        mock_connect.side_effect = Exception("DB connection failed")

        with pytest.raises(BlogError):
            create_post({'title': 'Test'})

    # Add similar tests for update_post, delete_post, get_all_posts