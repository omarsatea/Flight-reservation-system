import sqlite3
from sqlite3 import Error

def create_connection():
    """Create a database connection."""
    conn = None
    try:
        conn = sqlite3.connect('flights.db')
        print("Connection to SQLite DB successful")
        return conn
    except Error as e:
        print(f"Error: {e}")
    return conn

def create_table(conn):
    """Create reservations table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                departure TIME NOT NULL,
                destination TEXT NOT NULL,
                date DATE NOT NULL,
                seat_number TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Table created successfully")
    except Error as e:
        print(f"Error creating table: {e}")

def initialize_db():
    """Initialize the database and table."""
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()

if __name__ == "__main__":
    initialize_db()