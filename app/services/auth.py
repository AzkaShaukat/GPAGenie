import mysql.connector
from app.models.user import User
from app.utils.exceptions import AuthenticationError, RegistrationError

from passlib.hash import pbkdf2_sha256


class AuthService:
    # Hardcoded admin credentials
    ADMIN_CREDENTIALS = {
        "username": "admin",
        "password": "admin123",  # Default password
        "role": "admin",
        "full_name": "System Administrator"
    }

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def login(self, username, password):
        # First check if it's the hardcoded admin
        if username == self.ADMIN_CREDENTIALS["username"]:
            if password == self.ADMIN_CREDENTIALS["password"]:
                return User(
                    user_id=0,  # Special ID for hardcoded admin
                    username=self.ADMIN_CREDENTIALS["username"],
                    email="admin@gpagenie.com",
                    full_name=self.ADMIN_CREDENTIALS["full_name"],
                    role=self.ADMIN_CREDENTIALS["role"],
                    created_at=None,
                    last_login=None
                )
            raise AuthenticationError("Invalid admin password")

        # Normal user login from database
        cursor = self.db_connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )
            user_data = cursor.fetchone()

            if not user_data:
                raise AuthenticationError("Invalid username or password")

            if not pbkdf2_sha256.verify(password, user_data['password_hash']):
                raise AuthenticationError("Invalid username or password")

            # Update last login
            cursor.execute(
                "UPDATE users SET last_login = NOW() WHERE user_id = %s",
                (user_data['user_id'],)
            )
            self.db_connection.commit()

            return User(
                user_id=user_data['user_id'],
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                role=user_data['role'],
                created_at=user_data['created_at'],
                last_login=user_data['last_login']
            )
        except mysql.connector.Error as err:
            raise AuthenticationError(f"Database error: {err}")
        finally:
            cursor.close()

    # ... rest of the AuthService methods ...
    def logout(self):
        """Clear the current user session"""
        self.current_user = None
        return True

    # ... (keep existing register method and other code)

    def admin_exists(self):
        """Check if any admin user exists in the database"""
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            count = cursor.fetchone()[0]
            return count > 0
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return True  # Default to True for safety
        finally:
            cursor.close()

    def register(self, username, email, password, full_name, is_admin=False):
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            # Validate inputs
            username = User.validate_username(username)
            email = User.validate_email(email)
            User.validate_password(password)

            # Check if admin registration is allowed
            if is_admin and self.admin_exists():
                raise RegistrationError("Admin user already exists")

            # Check if username or email exists
            cursor.execute(
                "SELECT username, email FROM users WHERE username = %s OR email = %s",
                (username, email)
            )
            existing_users = cursor.fetchall()

            for user in existing_users:
                if user['username'] == username:
                    raise RegistrationError("Username already exists")
                if user['email'] == email:
                    raise RegistrationError("Email already registered")

            # Hash password
            hashed_password = User.hash_password(password)

            # Determine role
            role = 'admin' if is_admin else 'regular'

            # Insert new user
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, full_name, role) "
                "VALUES (%s, %s, %s, %s, %s)",
                (username, email, hashed_password, full_name, role)
            )
            self.db_connection.commit()

            # Get the new user
            user_id = cursor.lastrowid
            cursor.execute(
                "SELECT * FROM users WHERE user_id = %s",
                (user_id,)
            )
            user_data = cursor.fetchone()

            return User(
                user_id=user_data['user_id'],
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                role=user_data['role'],
                created_at=user_data['created_at']
            )
        except mysql.connector.Error as err:
            raise RegistrationError(f"Database error: {err}")
        finally:
            cursor.close()

