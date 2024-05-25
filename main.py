import streamlit as st
import pandas as pd
import requests
import time

# Add custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
        }
        .sidebar .sidebar-content {
            background-color: #e5e5e5;
        }
        .stButton>button {
            color: white;
            background-color: #4CAF50;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# Profile Button
st.sidebar.button("Profile", on_click=lambda: st.rerun())

# Button to manually set user as verified for testing
if st.sidebar.button("Set Verified"):
    st.session_state['profile'] = {
        "name": "Test User",
        "special_need": "None",
        "verified": "Verified"
    }
    st.rerun()

# Display user profile if verified
if 'profile' in st.session_state and st.session_state['profile']['verified'] == "Verified":
    profile = st.session_state['profile']
    st.sidebar.write("## User Profile")
    st.sidebar.write(f"**Name:** {profile['name']}")
    st.sidebar.write(f"**Special Need:** {profile['special_need']}")
else:
    st.sidebar.write("No verified profile found. Please complete your profile verification.")

# MRT stations import
mrtdata = pd.read_csv("mrt_lrt_data.csv")

# Display the columns of the DataFrame for debugging purposes
st.write("### DataFrame Columns:")
st.write(mrtdata.columns)

# Dropoff selection
st.header('Select the station you are getting off')

# Function to filter stations based on the search query
def filter_stations(query):
    if query:
        filtered_df = mrtdata[mrtdata['station_name'].str.contains(query, case=False, na=False)]
    else:
        filtered_df = mrtdata
    return filtered_df

st.title('MRT Cabin Status Updates')

# Convert station names to a list
station_names = mrtdata['station_name'].tolist()

# Search bar with autocomplete
search_query = st.text_input("Search for an MRT station:", "")

# Function to send notification
def send_notification():
    if 'profile' in st.session_state and st.session_state['profile']['verified'] == "Verified":
        profile = st.session_state['profile']
        notification = {
            "name": profile['name'],
            "special_need": profile['special_need'],
            "station": search_query
        }
        response = requests.post("http://localhost:5000/notify", json=notification)
        if response.status_code == 200:
            st.success("Notification sent successfully!")
        else:
            st.error("Failed to send notification.")

# Function to show Google Maps location using st.map
def show_location(station_name):
    station = mrtdata[mrtdata['station_name'] == station_name]
    if not station.empty:
        st.write("### Station Data:")
        st.write(station.iloc[0])
        
        # Use the correct column names based on the DataFrame inspection
        lat = station['latitude'].values[0]
        lon = station['longitude'].values[0]
        st.map(pd.DataFrame({
            'lat': [lat],
            'lon': [lon]
        }))

# App main function
def main():
    if search_query:
        if search_query in station_names:
            st.subheader("Selected Station")
            st.write(search_query)
            show_location(search_query)
            # Upload the selected station to the backend
            response = requests.post("http://localhost:5000/upload", json={"station": search_query})
            if response.status_code == 200:
                st.success("Station uploaded successfully!")
                if 'profile' in st.session_state and st.session_state['profile']['special_need']:
                    send_notification()
            else:
                st.error("Failed to upload station.")
        else:
            st.error("Invalid MRT station name.")
    else:
        st.info("Please enter a search query to find MRT stations.")

main()

# Retrieve uploaded data from the backend
if st.button("Get Uploaded Data"):
    response = requests.get("http://localhost:5000/data")
    if response.status_code == 200:
        uploaded_data = response.json().get("uploaded_data", [])
        st.subheader("Uploaded Stations")
        for station in uploaded_data:
            st.write(station)
    else:
        st.error("Failed to retrieve data.")

# Polling for notifications
def poll_notifications():
    while True:
        response = requests.get("http://localhost:5000/notifications")
        if response.status_code == 200:
            notifications = response.json().get("notifications", [])
            if notifications:
                for notification in notifications:
                    st.warning(f"Notification: {notification['name']} with special need '{notification['special_need']}' is leaving at {notification['station']}.")
        time.sleep(5)  # Poll every 5 seconds

# Start polling for notifications if the user is verified
if 'profile' in st.session_state and st.session_state['profile']['verified'] == "Verified":
    poll_notifications()