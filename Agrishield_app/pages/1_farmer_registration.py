import streamlit as st
import pandas as pd
import os

CSV_FILE = "farmers_data.csv"

st.set_page_config(page_title="Agrishield Insurance", page_icon="🌿", layout="wide")
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

# Load existing data if CSV exists
if os.path.exists(CSV_FILE):
    farmers_df = pd.read_csv(CSV_FILE)
else:
    farmers_df = pd.DataFrame(columns=["Name", "Email", "Age", "Farm Size", "Crop Type", "Insurance", "Climate Issue", "Province"])

# Registration Form
with st.form("farmer_form"):
    full_name = st.text_input("Full Name", value="")  # Blank field
    email = st.text_input("Email", value="")  # Blank field
    age = st.number_input("Age", min_value=18, max_value=100, value=None, step=1)  # Now blank
    farm_size = st.number_input("Farm Size (in acres)", min_value=0.1, step=0.1, value=None)  # Now blank
    crop_type = st.text_input("Primary Crop Type", value="")  # Blank field
    
    # Dropdowns with default "Select an option..." value
    insurance_options = ["Select an option...", "Basic Coverage", "Comprehensive Coverage", "Drought Protection", "Flood Protection"]
    insurance_type = st.selectbox("Insurance Type", insurance_options, index=0)

    climate_options = ["Select an option...", "Drought", "Flooding", "Extreme Heat", "Pest Infestation", "Other"]
    climate_issue = st.selectbox("Climate Issue Faced", climate_options, index=0)

    province_options = ["Select an option...", "Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan", "Gilgit-Baltistan", "Azad Jammu & Kashmir"]
    province = st.selectbox("Province", province_options, index=0)
    
    submit = st.form_submit_button("Register")

# If farmer submits the form
if submit:
    if not full_name or not email or age is None or farm_size is None or not crop_type \
       or insurance_type == "Select an option..." or climate_issue == "Select an option..." or province == "Select an option...":
        st.error("⚠️ Please fill in all required fields before submitting.")
    else:
        new_farmer = pd.DataFrame([[full_name, email, age, farm_size, crop_type, insurance_type, climate_issue, province]],
                                  columns=farmers_df.columns)
        
        farmers_df = pd.concat([farmers_df, new_farmer], ignore_index=True)  # Append new farmer
        farmers_df.to_csv(CSV_FILE, index=False)  # Save updated data

        st.session_state.farmers_data = farmers_df.to_dict(orient="records")  # Save to session state

        st.success(f"✅ Registration Successful!\n\n**Name:** {full_name}\n**Age:** {age} years")
        
        st.session_state.step = "insurance_payout"  # Move to next step
        
        # **🔹 Redirect to insurance payout page**
        st.switch_page("pages/2_insurance_payout.py")
