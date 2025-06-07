import mysql.connector
from app.utils.exceptions import BlogError
from app.utils.db_connector import Database  # Import the connector
from datetime import datetime


def get_all_published_posts():
    """Get all published blog posts from the database."""
    try:
        with Database() as conn:
            if conn is None:
                raise BlogError("Could not establish a database connection.")

            cursor = conn.cursor(dictionary=True)  # Use dictionary=True to get dict results

            query = """
                SELECT 
                    post_id, title, excerpt, content, featured_image, 
                    created_at, view_count, like_count 
                FROM blog_posts 
                WHERE status = 'published' 
                ORDER BY created_at DESC;
            """

            cursor.execute(query)
            posts = cursor.fetchall()

            if not posts:
                return []

            return posts

    except mysql.connector.Error as err:
        # Log the error in a real app
        raise BlogError(f"Database error while fetching posts: {err}")


# (Keep the rest of your functions like get_post_by_id, add_like, etc. as they are for now)
# You will need to implement them using the same 'with Database()' pattern.

def increment_view_count(post_id):
    """Increment the view count for a post"""
    try:
        # Implementation would update your database
        pass
    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")


def add_like(post_id, user_id):
    """Add a like to a blog post"""
    try:
        # Implementation would update your database
        pass
    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")


def get_post_comments(post_id):
    """Get comments for a blog post"""
    try:
        # Implementation would query your database
        return []  # Return empty list for now
    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")


def add_comment(post_id, user_id, author_name, content):
    """Add a new comment to a blog post"""
    try:
        # Implementation would insert into your database
        return {}  # Return empty dict for now
    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")