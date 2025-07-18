import os
import mysql.connector

class ExecuteQuery:
    def __init__(self, query, params):
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)

    with ExecuteQuery(query, params) as executor:
        for row in executor.results:
            print(row)