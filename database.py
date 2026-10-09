import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Ranju@123",
    "database": "bank_management_db",
    "port": 3306,
}

def get_connection():
    """Create and return a MySQL connection."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as exc:
        print(f"\nMySQL connection failed: {exc}")
        print("Check that MySQL Server is running and database.py has the correct password.")
        return None
