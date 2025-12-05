import sqlite3
import pandas as pd

# Connect to the DB
db_path = "database/jobs.db"
conn = sqlite3.connect(db_path)

def run_query(title, query):
    print(f"\n==========================================")
    print(f"📊 {title}")
    print(f"==========================================")
    try:
        df = pd.read_sql(query, conn)
        # Display full columns
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        print(df)
    except Exception as e:
        print(f"❌ Could not run query. Error: {e}")

# --- 1. CHECK COLUMNS ---
# We need to see the exact column names first!
print("🔎 INSPECTING DATABASE COLUMNS...")
schema_df = pd.read_sql("PRAGMA table_info(job_postings);", conn)
print(schema_df['name'].tolist())

# --- 2. ANALYZE JOB DEMAND (Count by Role) ---
query_demand = """
SELECT 
    job_title, 
    COUNT(*) as total_postings
FROM job_postings
GROUP BY job_title
ORDER BY total_postings DESC
LIMIT 10;
"""
run_query("Top 10 Most In-Demand Roles", query_demand)

# --- 3. ANALYZE SALARY (Avg Salary by Role) ---
# We assume 'salary_in_usd' exists based on dataset documentation
query_salary = """
SELECT 
    job_title, 
    ROUND(AVG(salary_in_usd), 0) as avg_salary_usd
FROM job_postings
GROUP BY job_title
HAVING COUNT(*) > 10  -- Only show roles with significant data
ORDER BY avg_salary_usd DESC
LIMIT 10;
"""
run_query("Top 10 Highest Paying Roles (Avg USD)", query_salary)

# --- 4. ANALYZE LOCATION (Where are the jobs?) ---
query_location = """
SELECT 
    company_location, 
    COUNT(*) as job_count,
    ROUND(AVG(salary_in_usd), 0) as avg_salary
FROM job_postings
GROUP BY company_location
ORDER BY job_count DESC
LIMIT 10;
"""
run_query("Top 10 Locations by Job Volume", query_location)

conn.close()