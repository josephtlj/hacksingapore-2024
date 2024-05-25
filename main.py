import streamlit as st
import pandas as pd
import numpy as np

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









#################

st.write('Headi')

# Import data using CSV
data = pd.read_csv("data.csv")
st.write(data)

# Text box
x = st.text_input("Favourite Movie")
st.write(f"Your favourite movie is: {x}")

# Button
is_clicked = st.button("Click Me")

# Chart
st.write("# My Cool Chart")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"]
)

st.bar_chart(chart_data)
st.line_chart(chart_data)

st.write("Headi")
