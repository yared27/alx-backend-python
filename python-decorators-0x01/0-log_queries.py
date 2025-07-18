import seed
from datetime import datetime
import functools
def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"Executing query: {query} at {datetime.now()}")
        return func(query, *args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = seed.connect_to_alx_prodev()
    if conn is None:
        print("Failed to connect to the database.")
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

users = fetch_all_users("SELECT * FROM user_data")
print(users)