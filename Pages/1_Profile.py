import streamlit as st

st.write("# Profile")

# Input fields for user information
name = st.text_input("Name")
email = st.text_input("Email")
ezlink_card = st.text_input("EZ-Link Card Number")
phone_number = st.text_input("Phone Number")

# SingPass login button (visual only)
st.button("SingPass Login")

st.write("## Special Need Request")

# Special Need
options = ["Pregnant", "Deaf", "Blind", "Physical Disability", "Elderly"]
selected_option = st.selectbox("Choose an option:", options)

# File upload section for verification documents
uploaded_file = st.file_uploader("Upload verification document")

# Placeholder for verification status
verification_status = "Not Verified"  # This should be manually toggled in the file for now

if st.button("Submit"):
    if uploaded_file is not None:
        verification_status = "Verified"
        st.success("Profile submitted for verification.")
    else:
        st.error("Please upload a verification document.")

# Store the user profile data in a session state
if verification_status == "Verified":
    st.session_state['profile'] = {
        'name': name,
        'email': email,
        'ezlink_card': ezlink_card,
        'phone_number': phone_number,
        'special_need': selected_option,
        'verified': verification_status,
    }