import streamlit as st

# Agrishield Branding
st.set_page_config(page_title="Agrishield Insurance", page_icon="🌿", layout="wide")

#st.image("agrishield_logo.png", width=150)  # Ensure the logo file is in your project folder
st.title("🌾 Climate-Affected Farmers Insurance Portal")
st.markdown(
    """
    <style>
        /* Dark background for the main app */
        body {
            background-color: #121212;
            color: white;
        }
        /* Blue sidebar with white text */
        [data-testid="stSidebar"] {
            background-color: #004080 !important;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        /* Style headers */
        h1, h2, h3, h4, h5, h6 {
            color: #00aaff;
        }
        /* Improve button styling */
        .stButton>button {
            background-color: #007acc;
            color: white;
            border-radius: 8px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #005f99;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = "registration"
if "farmers_data" not in st.session_state:
    st.session_state.farmers_data = []  # Ensuring it is always initialized



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
#cd "C:\Users\INDUS\Hasan Yasir, 22i-2251, FT-C, Agrishield app\Agrishield_app"
#streamlit run app.py
