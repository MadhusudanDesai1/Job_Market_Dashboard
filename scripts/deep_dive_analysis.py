import sqlite3
import pandas as pd

db_path = "database/jobs.db"
conn = sqlite3.connect(db_path)

def run_deep_dive(title, query):
    print(f"\n>>> 🎯 ANALYZING: {title}")
    try:
        df = pd.read_sql(query, conn)
        if df.empty:
            print("⚠ Warning: Result is empty. Check your filters.")
        else:
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print(df)
    except Exception as e:
        print(f"Error: {e}")

# --- 0. DIAGNOSTIC: CHECK YOUR VALUES ---
# This helps us see exactly how your data is named
print("\n--- 🔍 DIAGNOSTIC: DATA VALUES ---")
print("Unique Experience Levels:", pd.read_sql("SELECT DISTINCT experience_level FROM job_postings", conn)['experience_level'].tolist())
print("Unique Work Settings:", pd.read_sql("SELECT DISTINCT work_setting FROM job_postings", conn)['work_setting'].tolist())
print("------------------------------------\n")

# --- 1. THE "ENTRY-LEVEL" MARKET SCAN ---
# Updated to catch 'EN', 'Entry-level', or 'Entry Level'
q1 = """
SELECT 
    job_title,
    COUNT(*) as Openings,
    ROUND(AVG(salary_in_usd), 0) as Avg_Pay
FROM job_postings
WHERE experience_level IN ('EN', 'Entry-level', 'Entry Level') 
GROUP BY job_title
ORDER BY Openings DESC
LIMIT 10;
"""
run_deep_dive("Top Job Titles for Entry-Level Candidates", q1)

# --- 2. COMPANY SIZE & JUNIOR HIRING ---
# S = Small (<50), M = Medium (50-250), L = Large (>250)
q2 = """
SELECT 
    company_size,
    COUNT(*) as Junior_Hires,
    ROUND(AVG(salary_in_usd), 0) as Avg_Junior_Pay
FROM job_postings
WHERE experience_level IN ('EN', 'Entry-level', 'Entry Level')
GROUP BY company_size
ORDER BY Junior_Hires DESC;
"""
run_deep_dive("Who Hires Juniors? (Startups vs Corps)", q2)

# --- 3. THE "GOLDEN" JOBS (Entry Level + Fully Remote) ---
q3 = """
SELECT 
    company_location,
    COUNT(*) as Remote_Junior_Jobs,
    ROUND(AVG(salary_in_usd), 0) as Pay
FROM job_postings
WHERE experience_level IN ('EN', 'Entry-level', 'Entry Level')
  AND work_setting IN ('Remote', 'Fully Remote')
GROUP BY company_location
ORDER BY Remote_Junior_Jobs DESC
LIMIT 5;
"""
run_deep_dive("Top Countries for Remote Entry-Level Jobs", q3)

# --- 4. SALARY REALITY CHECK ---
q4 = """
SELECT 
    CASE 
        WHEN salary_in_usd < 50000 THEN 'Under $50k'
        WHEN salary_in_usd BETWEEN 50000 AND 100000 THEN '$50k - $100k'
        WHEN salary_in_usd BETWEEN 100000 AND 150000 THEN '$100k - $150k'
        ELSE 'Over $150k'
    END as Salary_Bracket,
    COUNT(*) as Job_Count
FROM job_postings
WHERE experience_level IN ('EN', 'Entry-level', 'Entry Level')
GROUP BY Salary_Bracket
ORDER BY Job_Count DESC;
"""
run_deep_dive("Salary Reality Check for Juniors", q4)

conn.close()