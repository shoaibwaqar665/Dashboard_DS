import csv
import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'corona',
    'user': 'postgres',
    'password': 'shoaib123',
    'host': 'localhost'  # Adjust as necessary
}

# Define the path to your CSV file
csv_file_path = 'corona/corona_NLP_test_annotated.csv'  # Ensure this path is correct

# Connect to your PostgreSQL database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Corrected SQL statement to create a table
create_table_sql = """
CREATE TABLE IF NOT EXISTS tweets (
    id SERIAL PRIMARY KEY,
    tweet TEXT NOT NULL,
    Prompt TEXT NOT NULL,
    generated_annotations TEXT NOT NULL,
    explanation TEXT
);
"""

try:
    # Create table
    cur.execute(create_table_sql)
    conn.commit()
    
    # Open the CSV file and insert each row into the table
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        next(csv_file)  # Skip the header row
        reader = csv.reader(csv_file)
        
        for row in reader:
            # Extracting data for each column from the row
            tweet = row[1]
            Prompt = row[2]
            generated_annotations = row[3]
            explanation = row[4]
            
            # SQL command for inserting data
            insert_sql = """
            INSERT INTO tweets (tweet, Prompt, generated_annotations, explanation)
            VALUES (%s, %s, %s, %s);
            """
            cur.execute(insert_sql, (tweet, Prompt, generated_annotations, explanation))
    
    conn.commit()
    print("Data imported successfully.")

except Exception as e:
    conn.rollback()  # Rollback the transaction in case of errors
    print(f"An error occurred: {e}")

finally:
    # Close the database connection
    cur.close()
    conn.close()
