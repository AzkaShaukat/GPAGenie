import re
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from app.utils.exceptions import ValidationError


class User:
    def __init__(self, user_id, username, email, full_name, role, created_at=None, last_login=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.role = role
        self.created_at = created_at or datetime.now()
        self.last_login = last_login

    @staticmethod
    def validate_username(username):
        if not username or len(username) < 4:
            raise ValidationError("Username must be at least 4 characters long")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers and underscores")
        return username

    @staticmethod
    def validate_email(email):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValidationError("Invalid email format")
        return email

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter")
        return password

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_password(password, hashed_password):
        return pbkdf2_sha256.verify(password, hashed_password)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "created_at": self.created_at,
            "last_login": self.last_login
        }