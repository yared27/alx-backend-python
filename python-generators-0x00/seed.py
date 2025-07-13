import mysql.connector
import os
from dotenv import load_dotenv
import csv
# Load environment variables from .env file
load_dotenv()


# Function to connect to the database
def connect_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT") 
        )
        print("Database connection successful")
        return connection
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        return None


# Function to create a database if it does not exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
        return None



# Function to connect to the ALX_prodev database
def connect_to_alx_prodev():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),  # Default to ALX_prodev if not set
            port=os.getenv("DB_PORT")  # Default to 3306 if not set
        )
        print("Connected to ALX_prodev database successfully")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None


# Function to create a table in the ALX_prodev database
def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age DECIMAL(3, 0) NOT NULL,
            INDEX (user_id)
            
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
        return None
    
# Function to insert data into the user_data table
def insert_data(connection, user_file):
    try:
        cursor = connection.cursor()
        with open(user_file, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            inserted = 0
            for row in reader:
                user_d = row["user_id"]
                name = row["name"]
                email = row["email"]
                age = row["age"]
                
                cursor.execute(
                    "SELECT 1 FROM user_data WHERE user_id = %s", (user_d,))
                if cursor.fetchone() :
                    continue  # Skip if user_id already exists
                insert_query = """INSERT INTO user_data (user_id, name, email, age) 
                                  VALUES (%s, %s, %s, %s)"""
                cursor.execute(insert_query, (user_d, name, email, age))
                inserted += 1
            connection.commit()
            print(f"Inserted {inserted} rows into user_data")
            cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        return None