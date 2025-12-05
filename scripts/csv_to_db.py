import pandas as pd
import sqlite3
import os

# Paths
csv_path = "data/jobs_data.csv"
db_path = "database/jobs.db"

# 1. Read the CSV
print("Reading CSV file...")
try:
    df = pd.read_csv(csv_path)
    print(f"✔ CSV read successfully. Found {len(df)} rows.")
except FileNotFoundError:
    print("❌ Error: CSV file not found. Did you run the previous step?")
    exit()

# 2. Clean Column Names
# SQL prefers snake_case (e.g., job_title) over spaces or camelCase.
# We map the likely CSV headers to clean SQL column names.
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

print("Columns cleaned:", df.columns.tolist())

# 3. Connect to SQLite (Creates the file if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 4. Write to SQL
# 'if_exists="replace"' means if we run this script twice, it won't duplicate data.
table_name = "job_postings"
df.to_sql(table_name, conn, if_exists='replace', index=False)

print(f"✔ Data successfully saved to SQLite database at: {db_path}")
print(f"  Table Name: {table_name}")

# 5. Sanity Check: Run a test query
print("\n--- TEST QUERY (Top 3 rows) ---")
test_query = f"SELECT * FROM {table_name} LIMIT 3;"
test_df = pd.read_sql(test_query, conn)
print(test_df)

# Close connection
conn.close()