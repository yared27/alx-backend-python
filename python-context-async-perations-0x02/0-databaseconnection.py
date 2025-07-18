from webbrowser import get
import mysql.connector
import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv()

class DatabaseConnection:
    def __init__(self, host, user, password, database, port=3306):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port
        }
        self.conn = None

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.config)
        if self.conn.is_connected():
            print("Database connection established.")   
            return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Database connection closed.")

with DatabaseConnection(os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME")) as conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    results = cursor.fetchall()
    cursor.close()
    print(results) if results else print("No data found.")