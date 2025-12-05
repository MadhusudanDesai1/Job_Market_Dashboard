# 📊 Data Science Job Market Dashboard (2024)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://madhusudandesai1-job-market-dashboard-app-wddgdf.streamlit.app)

## 📌 Project Overview

The tech job market is volatile. This project analyzes **14,000+ job postings** (2020-2024) to decode hiring trends in Data Science.

Rather than just making charts, I built an end-to-end data pipeline to simulate a real-world analytics workflow. I ingested raw data, engineered a relational database, ran complex SQL analysis to find "hidden" opportunities for entry-level candidates, and deployed a live interactive dashboard.

**Key Questions Answered:**

- **Strategy:** Which company size (Startup vs. Corp) offers the best odds for Junior Analysts?
- **Compensation:** What is the exact "Manager Premium" (pay increase) for leadership roles?
- **Market:** Does working remotely actually reduce your salary potential?

---

## ⚙️ Methodology: How I Built This (Step-by-Step)

I treated this project as a full-stack data engineering and analysis task, broken down into 4 phases:

### **Phase 1: Automated Data Ingestion (ETL)**

- **Goal:** Eliminate manual downloading and ensure data freshness.
- **Action:** I wrote a Python script (`ingest_data.py`) using the `kagglehub` API to automatically fetch the latest dataset versions.
- **Outcome:** A reproducible pipeline that keeps the raw data current without manual intervention.

### **Phase 2: Database Design & Modeling**

- **Goal:** Enable complex querying that isn't possible with static CSV files.
- **Action:** I designed a SQLite database schema and built an ETL script (`csv_to_db.py`) to:
  1.  Clean column names (standardizing to `snake_case`).
  2.  Handle missing values and data types.
  3.  Load the transformed data into a relational `jobs.db` database.
- **Why SQLite?** It offers the power of SQL for analytical queries while remaining lightweight for a portfolio project.

### **Phase 3: Strategic SQL Analysis**

- **Goal:** Derive insights that simple averages hide.
- **Action:** I utilized advanced SQL concepts in `deep_dive_analysis.py`, including:
  - **CASE Statements:** To categorize distinct salary bands and company sizes.
  - **Window Functions:** To rank companies by hiring volume.
  - **Aggregations:** To calculate the "Manager Premium."
    _Example SQL Logic used for segmentation:_
  ```sql
  SELECT
      CASE company_size
          WHEN 'S' THEN 'Small (Startup)'
          WHEN 'M' THEN 'Medium (Scale-up)'
          WHEN 'L' THEN 'Large (Corporation)'
      END as Company_Size,
      COUNT(*) as Junior_Hires
  FROM job_postings
  WHERE experience_level = 'EN'
  GROUP BY company_size
  ORDER BY Junior_Hires DESC;
  ```

### **Phase 4: Interactive Dashboarding**

- **Goal:** Make the insights accessible to non-technical stakeholders.
- **Action:** I built a **Streamlit** application (`app.py`) featuring:
  - **Dynamic Filtering:** Users can slice data by Role and Experience Level.
  - **Advanced Visuals:** Integrated **Plotly** for interactive box plots (showing salary distributions and outliers) and **Seaborn** for heatmaps.
  - **Real-time Metrics:** Key KPIs update instantly based on user selection.

---

## 🔍 Key Business Insights

My analysis revealed three counter-intuitive findings:

1.  **The "Mid-Size" Opportunity:** While Big Tech gets the attention, **Medium-sized companies (50-250 employees)** account for the highest volume of Entry-Level hires.
2.  **The Remote Myth:** Data shows that Remote roles pay within **5%** of on-site roles, suggesting that "location-based pay cuts" are fading in the data sector.
3.  **The Leadership Jump:** Transitioning from an Individual Contributor (IC) to a Manager role yields an average **35% salary increase**, validating the value of leadership tracks.

---

## 🛠️ Technical Stack

- **Language:** Python 3.10
- **Database:** SQLite3
- **Analysis:** SQL, Pandas
- **Visualization:** Streamlit, Plotly, Seaborn, Matplotlib
- **Version Control:** Git & GitHub

---

## 📂 Repository Structure

```bash
├── app.py                    # 📊 The Main Dashboard (Streamlit)
├── database/
│   └── jobs.db               # 🗄️ SQLite Database (The Single Source of Truth)
├── scripts/
│   ├── ingest_data.py        # ⬇️ Automated script to download data from Kaggle
│   ├── csv_to_db.py          # 🧹 ETL Pipeline: Cleans CSV and loads to SQL
│   ├── deep_dive_analysis.py # 🧠 Strategic SQL Analysis (The logic behind the insights)
│   └── salary_analysis.py    # 📉 Exploratory Data Analysis (Trends & Growth)
└── requirements.txt          # 📦 Dependencies
```
