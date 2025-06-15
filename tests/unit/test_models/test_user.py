import pytest
from datetime import datetime
from app.models.user import User, ValidationError
from passlib.hash import pbkdf2_sha256


class TestUserModel:
    def test_user_initialization(self):
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            role="regular"
        )

        assert user.user_id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.role == "regular"

    def test_validate_username_valid(self):
        assert User.validate_username("valid_user123") == "valid_user123"

        with pytest.raises(ValidationError):
            User.validate_username("invalid@user")

    def test_validate_email_valid(self):
        assert User.validate_email("test@example.com") == "test@example.com"

    def test_validate_email_invalid(self):
        with pytest.raises(ValidationError):
            User.validate_email("invalid-email")

    def test_validate_password_valid(self):
        assert User.validate_password("Valid1234") == "Valid1234"

    def test_validate_password_invalid(self):
        with pytest.raises(ValidationError):
            User.validate_password("short")

        with pytest.raises(ValidationError):
            User.validate_password("nouppercase1")

        with pytest.raises(ValidationError):
            User.validate_password("NODIGITS")

    def test_password_hashing(self):
        password = "TestPassword123"
        hashed = User.hash_password(password)

        assert pbkdf2_sha256.identify(hashed)
        assert User.verify_password(password, hashed)
        assert not User.verify_password("wrongpassword", hashed)