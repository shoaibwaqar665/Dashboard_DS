# import csv
# import psycopg2

# # Database connection parameters
# db_params = {
#     'dbname': 'corona',
#     'user': 'postgres',
#     'password': 'shoaib123',
#     'host': 'localhost'  # Adjust as necessary
# }

# # Define the path to your CSV file
# csv_file_path = 'corona/corona_NLP_test_annotated.csv'  # Ensure this path is correct

# # Connect to your PostgreSQL database
# conn = psycopg2.connect(**db_params)
# cur = conn.cursor()

# # Corrected SQL statement to create a table
# create_table_sql = """
# CREATE TABLE IF NOT EXISTS tweets (
#     id SERIAL PRIMARY KEY,
#     tweet TEXT NOT NULL,
#     Prompt TEXT NOT NULL,
#     generated_annotations TEXT NOT NULL,
#     explanation TEXT
# );
# """

# try:
#     # Create table
#     cur.execute(create_table_sql)
#     conn.commit()
    
#     # Open the CSV file and insert each row into the table
#     with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
#         next(csv_file)  # Skip the header row
#         reader = csv.reader(csv_file)
        
#         for row in reader:
#             # Extracting data for each column from the row
#             tweet = row[1]
#             Prompt = row[2]
#             generated_annotations = row[3]
#             explanation = row[4]
            
#             # SQL command for inserting data
#             insert_sql = """
#             INSERT INTO tweets (tweet, Prompt, generated_annotations, explanation)
#             VALUES (%s, %s, %s, %s);
#             """
#             cur.execute(insert_sql, (tweet, Prompt, generated_annotations, explanation))
    
#     conn.commit()
#     print("Data imported successfully.")

# except Exception as e:
#     conn.rollback()  # Rollback the transaction in case of errors
#     print(f"An error occurred: {e}")

# finally:
#     # Close the database connection
#     cur.close()
#     conn.close()


import pymysql
import csv
import glob
import os

# Database connection parameters
host = 'localhost'
user = 'root'
password = 'shoaib123'
database = 'hello'

# Directory where your CSV files are stored
directory_path = 'loc'

# Pattern to match all CSV files
file_pattern = os.path.join(directory_path, '*.csv')

# Connect to the database
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()

# SQL statement for creating the table with an auto-increment key
# create_table_sql = """
# CREATE TABLE IF NOT EXISTS locations (
#     `id` INT AUTO_INCREMENT PRIMARY KEY,
#     `name` TEXT,
#     `POI` TEXT,
#     `geometry` TEXT
# );
# """

# # Execute the SQL statement to create the table
# cursor.execute(create_table_sql)

# Function to insert data from a file into the database
# def insert_data_from_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header row
#         for row in reader:
#             insert_sql = "INSERT INTO locations (`geometry`) VALUES (%s)"
#             cursor.execute(insert_sql, row)
# Function to insert data from a file into the database
def insert_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            # Assuming geometry data is in the first column
            geometry_data = row[1]  # Adjust this index if necessary
            insert_sql = "INSERT INTO locations (`geometry`) VALUES (%s)"
            # Pass geometry_data within a tuple to match the single %s placeholder
            cursor.execute(insert_sql, (geometry_data,))

# List all CSV files and insert their data
for file_path in glob.glob(file_pattern):
    insert_data_from_file(file_path)

# Commit the transaction and close the connection
connection.commit()
connection.close()
