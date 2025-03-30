import streamlit as st
import pandas as pd
import os
import plotly.express as px

CSV_FILE = "farmers_data.csv"

st.title("💰 Insurance Payout Estimation")

# Ensure the farmer is registered
if not os.path.exists(CSV_FILE) or pd.read_csv(CSV_FILE).empty:
    st.warning("⚠️ Kindly register first in order to get further details.")
    st.stop()

# Load the latest registered farmer
farmers_df = pd.read_csv(CSV_FILE)
latest_farmer = farmers_df.iloc[-1]

# Read farmer details
st.write(f"👤 **Name:** {latest_farmer['Name']}")
st.write(f"📜 **Insurance Type:** {latest_farmer['Insurance']}")
st.write(f"☁️ **Climate Issue:** {latest_farmer['Climate Issue']}")

# Payout Calculation
payout_rate = {
    "Basic Coverage": 5000,
    "Comprehensive Coverage": 10000,
    "Drought Protection": 12000,
    "Flood Protection": 15000
}
base_payout = payout_rate.get(latest_farmer["Insurance"], 5000)

multiplier = {
    "Drought": 1.2,
    "Flooding": 1.5,
    "Extreme Heat": 1.1,
    "Pest Infestation": 1.3,
    "Other": 1.0
}.get(latest_farmer["Climate Issue"], 1.0)

estimated_payout = base_payout * latest_farmer["Farm Size"] * multiplier
st.metric(label="Estimated Payout", value=f"PKR {estimated_payout:,.0f}")

# 🔵 **Payout Increase Trend (Gradient Area Chart)**
payout_df = pd.DataFrame({
    "Farm Size (Acres)": range(1, 51),
    "Payout (PKR)": [base_payout * size * multiplier for size in range(1, 51)]
})

fig_payout = px.area(
    payout_df, x="Farm Size (Acres)", y="Payout (PKR)", 
    title="📈 Estimated Payout Increase by Farm Size",
    color_discrete_sequence=["#1f77b4"]
)
fig_payout.update_traces(fill='tozeroy', line=dict(width=2))


# 🟠 **Payout Distribution (Animated Donut Chart)**
payout_distribution = farmers_df["Insurance"].value_counts().reset_index()
payout_distribution.columns = ["Insurance Type", "Count"]

fig_donut = px.pie(
    payout_distribution, names="Insurance Type", values="Count",
    title="🟡 Payout Distribution by Insurance Type",
    hole=0.5, color_discrete_sequence=px.colors.sequential.Viridis
)
st.plotly_chart(fig_donut)

# Proceed Button
if st.button("➡ Proceed to Premium Charges"):
    st.session_state.step = "premium_charges"
    st.switch_page("pages/3_premium_charges.py")  # Switching to Premium Charges Page
