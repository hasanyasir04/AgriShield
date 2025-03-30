import streamlit as st
import pandas as pd
import os
import plotly.express as px

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
st.dataframe(filtered_df)

# Download Button
st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_farmers_data.csv",
    mime="text/csv"
)

# Summary Statistics
st.write("### 📊 Summary Statistics")
st.metric(label="Total Farmers (After Filters)", value=len(filtered_df))

# Graph 1: Pie Chart (Province Distribution)
if not filtered_df.empty:
    fig_pie = px.pie(filtered_df, names="Province", title="🗺️ Farmer Distribution by Province")
    st.plotly_chart(fig_pie)

# Graph 2: Histogram (Farm Size Distribution)
if not filtered_df.empty:
    fig_hist = px.histogram(filtered_df, x="Farm Size", nbins=20, title="📏 Farm Size Distribution")
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

    fig_box = px.box(filtered_df, y=["Premium", "Payout"], title="💰 Premium vs. Payout Analysis")
    st.plotly_chart(fig_box)
