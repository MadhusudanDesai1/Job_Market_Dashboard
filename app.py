import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 1. Setup Page
st.set_page_config(page_title="Data Job Market Dashboard", layout="wide")
st.title("📊 Data Science Job Market Dashboard (2024)")
st.markdown("Analyzing salaries, roles, and trends to find the best **Entry-Level Opportunities**.")

# 2. Connect to Data
@st.cache_data
def load_data():
    conn = sqlite3.connect("database/jobs.db")
    df = pd.read_sql("SELECT * FROM job_postings", conn)
    conn.close()
    return df

try:
    df = load_data()
    st.success(f"Data loaded successfully! {len(df)} records found.")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- DATA PRE-PROCESSING FOR ADVANCED ANALYSIS ---
def classify_role(title):
    title = str(title).lower()
    if any(x in title for x in ['lead', 'manager', 'principal', 'head', 'director']):
        return 'Leadership / Manager'
    elif 'senior' in title:
        return 'Senior IC'
    else:
        return 'Individual Contributor'

df['Role_Category'] = df['job_title'].apply(classify_role)

# 3. Sidebar Filters
st.sidebar.header("Filter Data")

# FIX 1: Added .tolist() to strictly convert Pandas Index to Python List
selected_role = st.sidebar.multiselect(
    "Select Job Title", 
    options=df['job_title'].unique().tolist(),
    default=df['job_title'].value_counts().index[:5].tolist()
)

selected_exp = st.sidebar.multiselect(
    "Select Experience Level",
    options=df['experience_level'].unique().tolist(),
    default=df['experience_level'].unique().tolist()
)

# Handle Empty Selection
if not selected_role:
    selected_role = df['job_title'].unique().tolist()
if not selected_exp:
    selected_exp = df['experience_level'].unique().tolist()

filtered_df = df[
    (df['job_title'].isin(selected_role)) & 
    (df['experience_level'].isin(selected_exp))
]

# 4. Key Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", len(filtered_df))
col2.metric("Avg Salary", f"${filtered_df['salary_in_usd'].mean():,.0f}")
col3.metric("Remote Jobs", len(filtered_df[filtered_df['work_setting'].isin(['Remote', 'Fully Remote'])]))
col4.metric("Leadership Roles", len(filtered_df[filtered_df['Role_Category'] == 'Leadership / Manager']))

st.markdown("---")

# ==============================================================================
# SECTION 1: ORIGINAL GRAPHS
# ==============================================================================
st.subheader("📈 Market Overview")
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("**💰 Salary Distribution** (Histogram)")
    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(filtered_df['salary_in_usd'], bins=20, kde=True, color='#4CAF50', ax=ax)
        ax.set_xlabel("Salary (USD)")
        st.pyplot(fig)

with col_right:
    st.markdown("**📅 Salary Growth Trend** (2020-2024)")
    if not filtered_df.empty:
        trend_data = filtered_df.groupby('work_year')['salary_in_usd'].mean()
        st.line_chart(trend_data)

# ==============================================================================
# SECTION 2: ADVANCED ANALYSIS
# ==============================================================================
st.markdown("---")
st.subheader("🚀 Advanced Career Insights")

# --- 1. BOX PLOT ---
st.markdown("### 1. Salary Ranges by Experience (Interactive)")
st.caption("Hover over the boxes to see the Median (middle line) and Outliers (dots).")
if not filtered_df.empty:
    fig_box = px.box(
        filtered_df, 
        x='experience_level', 
        y='salary_in_usd', 
        color='experience_level',
        points="outliers",
        title="Salary Distribution by Experience Level",
        category_orders={"experience_level": ["EN", "MI", "SE", "EX"]}
    )
    st.plotly_chart(fig_box, use_container_width=True)

# --- 2. MANAGER PREMIUM & 3. HEATMAP ---
col_adv1, col_adv2 = st.columns(2)

with col_adv1:
    st.markdown("### 2. The 'Manager Premium'")
    st.caption("How much more do 'Lead' or 'Manager' titles pay?")
    
    premium_data = df.groupby('Role_Category')['salary_in_usd'].mean().sort_values()
    
    # FIX 2: Fixed the typo (added space in 'except KeyError')
    try:
        ic_pay = premium_data['Individual Contributor']
        mgr_pay = premium_data['Leadership / Manager']
        diff = ((mgr_pay - ic_pay) / ic_pay) * 100
        st.info(f"💡 Insight: Leadership roles pay **{diff:.1f}% more** on average.")
    except KeyError:
        st.warning("Not enough data to calculate premium.")
        
    st.bar_chart(premium_data, color="#FF4B4B")

with col_adv2:
    st.markdown("### 3. Hiring Hotspots")
    st.caption("Darker squares = More jobs.")
    
    if not filtered_df.empty:
        heatmap_data = pd.crosstab(filtered_df['experience_level'], filtered_df['company_size'])
        
        fig_heat, ax_heat = plt.subplots(figsize=(6, 4))
        sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="Blues", ax=ax_heat)
        st.pyplot(fig_heat)

# ==============================================================================
# RAW DATA
# ==============================================================================
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df.head(100))