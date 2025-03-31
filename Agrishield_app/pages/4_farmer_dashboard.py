import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Apply Styling for a Professional Look
st.markdown(
    """
    <style>
        /* Background & Text Styling */
        body, .main {
            background-color: #F8F9FA !important;
            color: #212529 !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #004080 !important;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #004080 !important;
            font-weight: bold !important;
        }

        /* Buttons */
        .stButton > button {
            background-color: #007acc !important;
            color: white !important;
            border-radius: 10px !important;
            font-size: 16px !important;
            border: none !important;
            padding: 10px 18px !important;
        }
        .stButton > button:hover {
            background-color: #005f99 !important;
        }

        /* Data Table Styling */
        .stDataFrame, .stTable {
            background-color: #FFFFFF !important;
            color: black !important;
            border-radius: 5px !important;
        }

        /* Metric Styling */
        [data-testid="stMetric"] {
            background-color: #E9ECEF !important;
            color: #212529 !important;
            border-radius: 8px !important;
            padding: 12px !important;
            text-align: center !important;
        }

        /* Download Button */
        .stDownloadButton > button {
            background-color: #28a745 !important;
            color: white !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            padding: 10px 18px !important;
        }
        .stDownloadButton > button:hover {
            background-color: #218838 !important;
        }

    </style>
    """,
    unsafe_allow_html=True
)

CSV_FILE = "farmers_data.csv"

st.title("📊 Farmer Dashboard")

# Check if CSV file exists
if not os.path.exists(CSV_FILE) or pd.read_csv(CSV_FILE).empty:
    st.warning("⚠️ No farmers have registered yet.")
    st.stop()

# Load farmer data
farmers_df = pd.read_csv(CSV_FILE)

# Filters Section
st.sidebar.header("🔍 Filters")

# Province Filter
province_options = ["All"] + list(farmers_df["Province"].unique())
selected_province = st.sidebar.selectbox("📍 Select Province", province_options)

# Insurance Type Filter
insurance_options = ["All"] + list(farmers_df["Insurance"].unique())
selected_insurance = st.sidebar.selectbox("🛡️ Select Insurance Type", insurance_options)

# Apply Filters
filtered_df = farmers_df.copy()

if selected_province != "All":
    filtered_df = filtered_df[filtered_df["Province"] == selected_province]

if selected_insurance != "All":
    filtered_df = filtered_df[filtered_df["Insurance"] == selected_insurance]

# Search Feature
search_query = st.text_input("🔍 Search by Name or Email")
if search_query:
    filtered_df = filtered_df[
        filtered_df["Name"].str.contains(search_query, case=False, na=False) |
        filtered_df["Email"].str.contains(search_query, case=False, na=False)
    ]

# Display Data
st.write("### 📄 Filtered Farmer Data")
st.dataframe(filtered_df.style.set_properties(**{"background-color": "#FFFFFF", "color": "black"}))

# Download Button
st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_farmers_data.csv",
    mime="text/csv"
)

# Summary Statistics
st.write("### 📊 Summary Statistics")

col1, col2 = st.columns(2)
col1.metric(label="👨‍🌾 Total Farmers (After Filters)", value=len(filtered_df))
col2.metric(label="📏 Avg. Farm Size (acres)", value=f"{filtered_df['Farm Size'].mean():,.2f}" if not filtered_df.empty else "0")

# Graph 1: Pie Chart (Province Distribution)
if not filtered_df.empty:
    fig_pie = px.pie(
        filtered_df,
        names="Province",
        title="🗺️ Farmer Distribution by Province",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    fig_pie.update_layout(paper_bgcolor="#F8F9FA", font=dict(color="black"))
    st.plotly_chart(fig_pie)

# Graph 2: Histogram (Farm Size Distribution)
if not filtered_df.empty:
    fig_hist = px.histogram(
        filtered_df,
        x="Farm Size",
        nbins=20,
        title="📏 Farm Size Distribution",
        color_discrete_sequence=["#004080"]
    )
    fig_hist.update_layout(paper_bgcolor="#F8F9FA", font=dict(color="black"))
    st.plotly_chart(fig_hist)

# Graph 3: Box Plot (Premium vs Payout)
if "Insurance" in filtered_df.columns:
    premium_rates = {
        "Basic Coverage": 1000,
        "Comprehensive Coverage": 2500,
        "Drought Protection": 3000,
        "Flood Protection": 3500
    }
    payout_rates = {
        "Basic Coverage": 5000,
        "Comprehensive Coverage": 10000,
        "Drought Protection": 12000,
        "Flood Protection": 15000
    }

    filtered_df["Premium"] = filtered_df["Insurance"].map(premium_rates) * filtered_df["Farm Size"]
    filtered_df["Payout"] = filtered_df["Insurance"].map(payout_rates) * filtered_df["Farm Size"]

    fig_box = px.box(
        filtered_df,
        y=["Premium", "Payout"],
        title="💰 Premium vs. Payout Analysis",
        color_discrete_sequence=["#007acc", "#28a745"]
    )
    fig_box.update_layout(paper_bgcolor="#F8F9FA", font=dict(color="black"))
    st.plotly_chart(fig_box)

