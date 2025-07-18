import mysql.connector
import seed

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        conn = seed.connect_to_alx_prodev()
        if conn is None:
            print("Failed to connect to the database.")
            return None
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
    return cursor.fetchone()

user = get_user_by_id(user_id=1)
print(user) if user else print("User not found")