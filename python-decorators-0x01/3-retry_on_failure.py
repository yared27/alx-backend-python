import seed
import functools
import time

def with_db_connection(func):
    @functools.wraps(func)
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

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    last_exception = e
                    if attempt < retries - 1:
                        time.sleep(delay)
            print("All attempts failed.")
            return last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=5, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    results = cursor.fetchall()
    cursor.close()
    return results


try:
    users = fetch_users_with_retry()
    print(users)
except Exception as e:
    print(f"Failed to fetch users: {e}")
