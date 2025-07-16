import mysql.connector
import os
from dotenv import load_dotenv
import seed

load_dotenv()

def stream_users():
    try:
        conn = seed.connect_to_alx_prodev()
        if conn is None:
                print("Failed to connect to the database.")
                return
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
       print(f"Error streaming users: {err}")
       return  
