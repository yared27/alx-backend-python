import seed
import functools

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

def cache_query(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in cache:
            print("Returning cached result for query:", query)
            return cache[query]
        result = func(conn, query, *args, **kwargs)
        cache[query] = result
        return result

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results
users = fetch_users_with_cache("SELECT * FROM user_data")
print(users)

# Usage
users_again = fetch_users_with_cache("SELECT * FROM user_data")
print(users_again)