import mysql.connector
from app.utils.exceptions import BlogError
from app.utils.db_connector import Database  # Import the connector
from datetime import datetime

def get_all_posts():
    """Get all blog posts (for admin)"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gpa_genie1"
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM blog_posts 
            ORDER BY created_at DESC
        """)
        posts = cursor.fetchall()

        cursor.close()
        connection.close()

        return posts

    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")

def create_post(post_data):
    """Create a new blog post"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gpa_genie1"
        )
        cursor = connection.cursor()

        # Use the user_id from the user object if available, otherwise prompt or default
        author_id = post_data.get('author_id')
        if not author_id:
            raise BlogError("Author ID is required. Please ensure a valid user is logged in.")

        # Validate author_id exists in users table
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (author_id,))
        if cursor.fetchone() is None:
            raise BlogError(f"Author ID {author_id} does not exist in the users table.")

        query = """
        INSERT INTO blog_posts 
        (title, excerpt, content, featured_image, author_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """

        values = (
            post_data['title'],
            post_data['excerpt'],
            post_data['content'],
            post_data.get('featured_image'),
            author_id
        )

        cursor.execute(query, values)
        connection.commit()

        return cursor.lastrowid

    except mysql.connector.Error as err:
        connection.rollback()
        raise BlogError(f"Database error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_post(post_data):
    """Update existing blog post"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gpa_genie1"
        )
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE blog_posts SET
                title = %s,
                content = %s,
                excerpt = %s,
                featured_image = %s,
                status = %s,
                updated_at = NOW()
            WHERE post_id = %s
        """, (
            post_data['title'],
            post_data['content'],
            post_data['excerpt'],
            post_data['featured_image'],
            post_data.get('status', 'published'),
            post_data['post_id']
        ))

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")

def delete_post(post_id):
    """Delete blog post"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gpa_genie1"
        )
        cursor = connection.cursor()

        # First delete comments
        cursor.execute("DELETE FROM blog_comments WHERE post_id = %s", (post_id,))

        # Then delete post
        cursor.execute("DELETE FROM blog_posts WHERE post_id = %s", (post_id,))

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")

def get_all_published_posts():
    """Get all published blog posts from the database."""
    try:
        with Database() as conn:
            if conn is None:
                raise BlogError("Could not establish a database connection.")

            cursor = conn.cursor(dictionary=True)

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
        raise BlogError(f"Database error while fetching posts: {err}")

def increment_view_count(post_id):
    """Increment the view count for a post"""
    try:
        pass
    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")

def add_like(post_id, user_id):
    """Add a like to a blog post"""
    try:
        pass
    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")

def get_post_comments(post_id):
    """Get comments for a blog post"""
    try:
        return []
    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")

def add_comment(post_id, user_id, author_name, content):
    """Add a new comment to a blog post"""
    try:
        return {}
    except mysql.connector.Error as err:
        raise BlogError(f"Database error: {err}")