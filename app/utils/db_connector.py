import mysql.connector
from mysql.connector import Error

# --- IMPORTANT ---
# Replace these with your actual database credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'gpa_genie1'
}

class Database:
    """A context manager for handling database connections."""
    def __init__(self):
        self._connection = None

    def __enter__(self):
        try:
            self._connection = mysql.connector.connect(**DB_CONFIG)
            return self._connection
        except Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection and self._connection.is_connected():
            self._connection.close()