import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px

# Sidebar and Page Styling
st.markdown(
    """
    <style>
    body, .main { background-color: #FFFFFF !important; color: black !important; }
    [data-testid="stSidebar"] { background-color: #004080 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
      width: 200px !important;
    h1, h2, h3, h4, h5, h6 { color: #004080 !important; }
    .stButton > button {
        background-color: #007acc !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-size: 16px !important;
    }
    .stButton > button:hover { background-color: #005f99 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

CSV_FILE = "farmers_data.csv"
st.title("💳 Agrishield Premium Charges")

# Ensure the farmer is registered
if not os.path.exists(CSV_FILE) or pd.read_csv(CSV_FILE).empty:
    st.warning("⚠️ Kindly register first in order to get further details.")
    st.stop()

# Load data
farmers_df = pd.read_csv(CSV_FILE)
latest_farmer = farmers_df.iloc[-1]

# Read farmer details
st.write(f"👤 **Name:** {latest_farmer['Name']}")
st.write(f"📍 **Province:** {latest_farmer['Province']}")
st.write(f"🌾 **Farm Size:** {latest_farmer['Farm Size']} acres")
st.write(f"📜 **Insurance Type:** {latest_farmer['Insurance']}")

# Premium Calculation
premium_rates = {
    "Basic Coverage": 1000,
    "Comprehensive Coverage": 2500,
    "Drought Protection": 3000,
    "Flood Protection": 3500
}
base_premium = premium_rates.get(latest_farmer["Insurance"], 1000)
annual_premium = base_premium * latest_farmer["Farm Size"]
st.metric(label="Annual Premium", value=f"PKR {annual_premium:,.0f}")

# Performance Indicators
total_farmers = len(farmers_df)
total_farm_area = farmers_df["Farm Size"].sum()
total_premium_collected = (farmers_df["Farm Size"] * farmers_df["Insurance"].map(premium_rates)).sum()

col1, col2, col3 = st.columns(3)
col1.metric(label="👨‍🌾 Total Farmers Registered", value=total_farmers)
col2.metric(label="🌍 Total Insured Farm Area (acres)", value=f"{total_farm_area:,.0f}")
col3.metric(label="💰 Total Premium Collected (PKR)", value=f"{total_premium_collected:,.0f}")

# 📊 **Stacked Area Chart: Premium & Farm Size by Province**
province_data = farmers_df.groupby("Province").agg({"Farm Size": "sum"}).reset_index()
province_data["Total Premium"] = province_data["Farm Size"] * base_premium

if not province_data.empty:
    stacked_area_fig = px.area(
        province_data,
        x="Province",
        y=["Farm Size", "Total Premium"],
        labels={"value": "Amount", "variable": "Category"},
        title="📊 Stacked Area Chart - Premium & Farm Size by Province",
        color_discrete_sequence=["#FF5733", "#1E90FF"]
    )
    stacked_area_fig.update_layout(
        xaxis_title="Province",
        yaxis_title="Value",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="black")
    )
    st.plotly_chart(stacked_area_fig)

# 🥧 **Pie Chart: Insurance Type Distribution**
insurance_counts = farmers_df["Insurance"].value_counts().reset_index()
insurance_counts.columns = ["Insurance Type", "Count"]

pie_fig = px.pie(insurance_counts, names="Insurance Type", values="Count",
                 title="📊 Insurance Type Distribution",
                 color_discrete_sequence=px.colors.qualitative.Set1)
pie_fig.update_traces(textposition="inside", textinfo="percent+label")
pie_fig.update_layout(paper_bgcolor="#FFFFFF", font=dict(color="black"))
st.plotly_chart(pie_fig)

# 🔢 **Interactive Slider for Custom Calculation**
st.write("### 🔢 Adjust Farm Size to See Premium Changes")
custom_farm_size = st.slider("Farm Size (acres)", min_value=0.5, max_value=50.0, step=0.5, value=latest_farmer["Farm Size"])
custom_premium = base_premium * custom_farm_size
st.metric(label="Updated Premium", value=f"PKR {custom_premium:,.0f}")

# ✅ **Proceed Button**
if st.button("✅ Complete & View Dashboard"):
    st.session_state.step = "farmer_dashboard"
    st.switch_page("pages/4_farmer_dashboard.py")
