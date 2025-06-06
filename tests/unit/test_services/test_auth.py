import pytest
from unittest.mock import MagicMock
from app.services.auth import AuthService
from app.models.user import User
from app.utils.exceptions import AuthenticationError, RegistrationError
import mysql.connector


class TestAuthService:
    @pytest.fixture
    def mock_db(self):
        mock = MagicMock()
        mock.cursor.return_value = MagicMock()
        return mock

    def test_login_success(self, mock_db):
        # Setup mock database response
        cursor = mock_db.cursor.return_value
        cursor.fetchone.return_value = {
            'user_id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'full_name': 'Test User',
            'role': 'regular',
            'password_hash': User.hash_password('correctpass'),
            'created_at': '2023-01-01 00:00:00',
            'last_login': None
        }

        auth_service = AuthService(mock_db)
        user = auth_service.login('testuser', 'correctpass')

        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert isinstance(user, User)

    def test_login_invalid_username(self, mock_db):
        cursor = mock_db.cursor.return_value
        cursor.fetchone.return_value = None

        auth_service = AuthService(mock_db)

        with pytest.raises(AuthenticationError):
            auth_service.login('nonexistent', 'password')

    def test_login_invalid_password(self, mock_db):
        cursor = mock_db.cursor.return_value
        cursor.fetchone.return_value = {
            'user_id': 1,
            'username': 'testuser',
            'password_hash': User.hash_password('correctpass'),
            # other fields...
        }

        auth_service = AuthService(mock_db)

        with pytest.raises(AuthenticationError):
            auth_service.login('testuser', 'wrongpass')

    def test_register_success(self, mock_db):
        cursor = mock_db.cursor.return_value
        cursor.fetchall.return_value = []
        cursor.lastrowid = 1
        cursor.fetchone.return_value = {
            'user_id': 1,
            'username': 'newuser',
            'email': 'new@example.com',
            'full_name': 'New User',
            'role': 'regular',
            'created_at': '2023-01-01 00:00:00'
        }

        auth_service = AuthService(mock_db)
        user = auth_service.register(
            username='newuser',
            email='new@example.com',
            password='ValidPass123',
            full_name='New User'
        )

        assert user.username == 'newuser'
        assert isinstance(user, User)

    def test_register_existing_username(self, mock_db):
        cursor = mock_db.cursor.return_value
        cursor.fetchall.return_value = [('existinguser', 'other@example.com')]

        auth_service = AuthService(mock_db)

        with pytest.raises(RegistrationError):
            auth_service.register(
                username='existinguser',
                email='new@example.com',
                password='ValidPass123',
                full_name='New User'
            )

    def test_register_existing_email(self, mock_db):
        cursor = mock_db.cursor.return_value
        cursor.fetchall.return_value = [('otheruser', 'existing@example.com')]

        auth_service = AuthService(mock_db)

        with pytest.raises(RegistrationError):
            auth_service.register(
                username='newuser',
                email='existing@example.com',
                password='ValidPass123',
                full_name='New User'
            )