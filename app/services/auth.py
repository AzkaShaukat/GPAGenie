import mysql.connector
from app.models.user import User
from app.utils.exceptions import AuthenticationError, RegistrationError


class AuthService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def login(self, username, password):
        cursor = self.db_connection.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )
            user_data = cursor.fetchone()

            if not user_data:
                raise AuthenticationError("Invalid username or password")

            if not User.verify_password(password, user_data['password_hash']):
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

    def register(self, username, email, password, full_name):
        cursor = self.db_connection.cursor(dictionary=True)  # Changed to dictionary cursor

        try:
            # Validate inputs
            username = User.validate_username(username)
            email = User.validate_email(email)
            User.validate_password(password)

            # Check if username or email already exists
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

            # Insert new user
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, full_name, role) "
                "VALUES (%s, %s, %s, %s, 'regular')",
                (username, email, hashed_password, full_name)
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