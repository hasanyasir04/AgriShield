import streamlit as st

# Agrishield Branding
st.set_page_config(page_title="Agrishield Insurance", page_icon="🌿", layout="wide")

#st.image("agrishield_logo.png", width=150)  # Ensure the logo file is in your project folder
st.title("🌾 Climate-Affected Farmers Insurance Portal")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = "registration"
if "farmers_data" not in st.session_state:
    st.session_state.farmers_data = []  # Ensuring it is always initialized

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.session_state.farmers_data:
    farmer = st.session_state.farmers_data[-1]
    st.sidebar.write(f"👤 **Farmer Name:** {farmer['Name']}")
    st.sidebar.write(f"🎂 **Age:** {farmer['Age']} years")

# Page Navigation
if st.session_state.step == "registration":
    st.write("### Register as a Farmer to Proceed")
    if st.button("➡ Proceed to Registration"):
        st.session_state.step = "insurance_payout"
        st.switch_page("pages/1_farmer_registration.py")

elif st.session_state.step == "insurance_payout":
    if not st.session_state.farmers_data:
        st.warning("⚠️ Kindly register first in order to get further details.")
    else:
        st.write("### View Your Insurance Payout Estimation")
        if st.button("➡ View Payout Estimation"):
            st.session_state.step = "premium_charges"
            st.switch_page("pages/2_insurance_payout.py")

elif st.session_state.step == "premium_charges":
    if not st.session_state.farmers_data:
        st.warning("⚠️ Kindly register first in order to get further details.")
    else:
        st.write("### Review Your Premium Charges")
        if st.button("➡ Review Premium Charges"):
            st.session_state.step = "thank_you"
            st.switch_page("pages/3_premium_charges.py")

elif st.session_state.step == "thank_you":
    st.success("✅ Thank you for registering! Your insurance is now active.")
