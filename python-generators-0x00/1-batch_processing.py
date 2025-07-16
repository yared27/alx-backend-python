import mysql.connector
import os
import seed
from dotenv import load_dotenv

load_dotenv()

def stream_users_in_batches(batch_size):
    try:
        conn = seed.connect_to_alx_prodev()
        if conn is None:
            print("Failed to connect to the database.")
            return
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error streaming users in batches: {err}")
        return  
    
def batch_processing(batch_size):
    for user in stream_users_in_batches(batch_size):
        # Process each user here
        if user["age"] > 25:
            print(user)