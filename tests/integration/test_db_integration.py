import pytest
from app.services.blog_service import create_post
from app.services import databse


@pytest.mark.integration
class TestBlogDBIntegration:
    def test_create_post_with_default_author(self, test_db):
        """Test actual database insertion with default author"""
        post_data = {
            'title': 'DB Integration Test',
            'excerpt': 'Test excerpt',
            'content': 'Test content'
            # No author_id provided
        }

        post_id = create_post(post_data)

        # Verify record was created with author_id=1
        with databse.cursor() as cursor:
            cursor.execute("SELECT author_id FROM blog_posts WHERE post_id = %s", (post_id,))
            result = cursor.fetchone()
            assert result[0] == 1

    def test_foreign_key_constraint(self, test_db):
        """Verify foreign key constraint works"""
        # First ensure user with ID 1 exists
        with databse.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (user_id, username) 
                VALUES (1, 'test_admin')
                ON DUPLICATE KEY UPDATE username='test_admin'
            """)
            databse.commit()

        # Now test post creation
        post_data = {
            'title': 'Constraint Test',
            'content': 'Should work with author_id=1'
        }

        post_id = create_post(post_data)
        assert post_id is not None