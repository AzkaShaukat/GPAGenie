import pytest
import mysql.connector
from mysql.connector import Error
import time
from app.main import GPAGenieApp
from app.services.auth import AuthService
from app.models.user import User
from app.utils.exceptions import AuthenticationError, RegistrationError


class TestAuthIntegration:
    @pytest.fixture(scope='session')
    def db_connection(self):
        """Session-level fixture for database connection"""
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                # Connect without specifying database first
                admin_conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    port=3306
                )

                # Create test database if needed
                cursor = admin_conn.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS gpa_genie1_test")
                admin_conn.commit()
                cursor.close()
                admin_conn.close()

                # Now connect to test database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="gpa_genie1_test",
                    port=3306
                )

                # Verify connection works
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()

                return conn

            except Error as e:
                if attempt == max_retries - 1:
                    pytest.skip(f"Could not connect to MySQL after {max_retries} attempts: {e}")
                time.sleep(retry_delay)

    @pytest.fixture
    def app(self, db_connection):
        """Create test tables and app instance"""
        if db_connection is None:
            pytest.skip("Database connection not available")

        # Create tables with explicit error handling
        cursor = db_connection.cursor()
        try:
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
                ) ENGINE=InnoDB
            """)
            db_connection.commit()
        except Error as e:
            pytest.fail(f"Failed to create users table: {e}")
        finally:
            cursor.close()

        app = GPAGenieApp()
        app.db_connection = db_connection
        app.auth_service = AuthService(db_connection)

        yield app

        # Cleanup - only drop data, not tables
        cursor = db_connection.cursor()
        try:
            cursor.execute("DELETE FROM users")
            db_connection.commit()
        finally:
            cursor.close()

    def test_register_and_login_flow(self, app):
        """Test complete registration and login flow"""
        # Verify table exists before test
        cursor = app.db_connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'users'")
        assert cursor.fetchone() is not None, "Users table does not exist"
        cursor.close()

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