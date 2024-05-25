import streamlit as st
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

# Profile Button
st.sidebar.button("Profile", on_click=lambda: st.experimental_rerun())

# Display user profile if verified
if 'profile' in st.session_state and st.session_state['profile']['verified'] == "Verified":
    profile = st.session_state['profile']
    st.write("## User Profile")
    st.write(f"**Name:** {profile['name']}")
    st.write(f"**Special Need:** {profile['special_need']}")
else:
    st.write("No verified profile found. Please complete your profile verification.")

# MRT stations import
mrtdata = pd.read_csv("mrt_lrt_data.csv")

# Dropoff selection
st.title('Select the station you are getting off')

# Finding station from dataset
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

# App function
def main():

    if search_query:
        if search_query in station_names:
            st.write("### Selected Station")
            st.write(search_query)
        else:
            st.write("Invalid MRT station name.")
    else:
        st.write("Please enter a search query to find MRT stations.")

main()



app = Flask(__name__)

# In-memory storage for simplicity
uploaded_data = []

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    stations = search_query
    if stations:
        uploaded_data.extend(stations)
        return jsonify({"message": "Stations uploaded successfully!"}), 200
    return jsonify({"message": "No stations provided."}), 400

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({"uploaded_data": uploaded_data}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
