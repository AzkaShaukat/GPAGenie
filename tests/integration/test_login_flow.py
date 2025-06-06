import pytest
from app.main import GPAGenieApp
from app.models.user import User
import mysql.connector


class TestAuthIntegration:
    @pytest.fixture
    def app(self):
        # Setup test database connection
        db_conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gpa_genie1_test"  # Use a test database
        )

        # Create test tables
        cursor = db_conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                role ENUM('admin','regular') DEFAULT 'regular',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        """)
        db_conn.commit()
        cursor.close()

        # Create test app instance
        app = GPAGenieApp()
        app.db_connection = db_conn
        app.auth_service = AuthService(db_conn)

        yield app

        # Cleanup
        cursor = db_conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        db_conn.commit()
        db_conn.close()

    def test_register_and_login_flow(self, app):
        # Test registration
        test_user = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'full_name': 'Test User'
        }

        # Register new user
        user = app.auth_service.register(**test_user)
        assert isinstance(user, User)
        assert user.username == test_user['username']

        # Test login with correct credentials
        logged_in_user = app.auth_service.login(test_user['username'], test_user['password'])
        assert logged_in_user.user_id == user.user_id

        # Test login with incorrect password
        with pytest.raises(AuthenticationError):
            app.auth_service.login(test_user['username'], 'wrongpass')