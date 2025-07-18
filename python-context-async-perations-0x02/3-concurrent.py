import asyncio
import mysql.connector
import seed

def fetch_all_users(query):
    conn = seed.connect_to_alx_prodev()
    if conn is None:
        print("Failed to connect to the database.")
        return []   
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users " )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def fetch_older_users(query):
    conn = seed.connect_to_alx_prodev()
    if conn is None:
        print("Failed to connect to the database.")
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE age > 40")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

async def async_fetch_all_users(query):
    return await asyncio.to_thread(fetch_all_users, query)

async def async_fetch_older_users(query):
    return await asyncio.to_thread(fetch_older_users, query)

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_all_users("SELECT * FROM users"),
        async_fetch_older_users("SELECT * FROM users WHERE age > 40")
    )

    print("All Users:")
    for user in all_users:
        print(user)
    print("Older Users:")
    for user in older_users:
        print(user)
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())