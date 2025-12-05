import sqlite3
import pandas as pd

db_path = "database/jobs.db"
conn = sqlite3.connect(db_path)

# Helper function to make output pretty
def show_query(title, query):
    print(f"\n--- {title} ---")
    try:
        df = pd.read_sql(query, conn)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        print(df)
    except Exception as e:
        print(f"Error: {e}")

# 1. SALARY BY EXPERIENCE LEVEL
# (EN = Entry, MI = Mid, SE = Senior, EX = Executive)
q1 = """
SELECT 
    CASE experience_level 
        WHEN 'EN' THEN 'Entry-Level'
        WHEN 'MI' THEN 'Mid-Level'
        WHEN 'SE' THEN 'Senior'
        WHEN 'EX' THEN 'Executive'
    END as Experience,
    COUNT(*) as Job_Count,
    ROUND(AVG(salary_in_usd), 0) as Avg_Salary_USD
FROM job_postings
GROUP BY experience_level
ORDER BY Avg_Salary_USD DESC;
"""
show_query("Salary vs Experience Level", q1)

# 2. REMOTE VS IN-PERSON SALARIES
# Does working from home pay more?
q2 = """
SELECT 
    work_setting,
    COUNT(*) as Job_Count,
    ROUND(AVG(salary_in_usd), 0) as Avg_Salary_USD
FROM job_postings
GROUP BY work_setting
ORDER BY Avg_Salary_USD DESC;
"""
show_query("Remote vs On-Site Salary Trends", q2)

# 3. TRENDS OVER YEARS (2020-2024)
# Are salaries going up or down?
q3 = """
SELECT 
    work_year,
    COUNT(*) as Total_Jobs,
    ROUND(AVG(salary_in_usd), 0) as Avg_Salary
FROM job_postings
GROUP BY work_year
ORDER BY work_year ASC;
"""
show_query("Salary Growth Over Time", q3)

# 4. HIGHEST PAYING JOB CATEGORIES
q4 = """
SELECT 
    job_category,
    ROUND(AVG(salary_in_usd), 0) as Avg_Salary
FROM job_postings
GROUP BY job_category
ORDER BY Avg_Salary DESC;
"""
show_query("Best Paying Data Categories", q4)

conn.close()