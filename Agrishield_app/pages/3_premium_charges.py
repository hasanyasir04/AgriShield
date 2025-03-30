import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

CSV_FILE = "farmers_data.csv"

st.title("💳 Agrishield Premium Charges")

# Ensure the farmer is registered
if not os.path.exists(CSV_FILE) or pd.read_csv(CSV_FILE).empty:
    st.warning("⚠️ Kindly register first in order to get further details.")
    st.stop()

# Load the latest registered farmer
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

# 📊 **Waterfall Chart: Premium Contribution by Province**
province_data = farmers_df.groupby("Province").agg({"Farm Size": "mean"}).reset_index()
province_data["Average Premium"] = province_data["Farm Size"] * base_premium

if not province_data.empty:
    waterfall_fig = go.Figure(go.Waterfall(
        name="Average Premium",
        orientation="v",
        measure=["relative"] * len(province_data),  # All bars as 'relative' increases
        x=province_data["Province"],
        y=province_data["Average Premium"],
        text=[f"PKR {value:,.0f}" for value in province_data["Average Premium"]],
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "red"}},
        increasing={"marker": {"color": "#1f77b4"}},
    ))

    waterfall_fig.update_layout(
        title="📊 Premium Contribution by Province",
        xaxis_title="Province",
        yaxis_title="Average Premium (PKR)"
    )

    st.plotly_chart(waterfall_fig)

# 🔢 **Interactive Slider for Custom Calculation**
st.write("### 🔢 Adjust Farm Size to See Premium Changes")
custom_farm_size = st.slider("Farm Size (acres)", min_value=0.5, max_value=50.0, step=0.5, value=latest_farmer["Farm Size"])
custom_premium = base_premium * custom_farm_size
st.metric(label="Updated Premium", value=f"PKR {custom_premium:,.0f}")

# ✅ **Proceed Button**
if st.button("✅ Complete & View Dashboard"):
    st.session_state.step = "farmer_dashboard"
    st.switch_page("pages/4_farmer_dashboard.py")  # Switching to Dashboard Page
