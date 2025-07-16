import mysql.connector
import os
from dotenv import load_dotenv
import seed

load_dotenv()

def stream_user_ages():
    try:
        conn = seed.connect_to_alx_prodev()
        if conn is None:
            print("Failed to connect to the database.")
            return
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row['age']

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error streaming user ages: {err}")
        return
def compute_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count == 0:
        print("No users found.")
        return
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")