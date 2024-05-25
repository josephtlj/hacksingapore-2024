import streamlit as st
import pandas as pd
import numpy as np



# Profile Button
st.link_button("Profile", "http://localhost:8501/profile")

# Display user profile if verified
if 'profile' in st.session_state and st.session_state['profile']['verified'] == "Verified":
    profile = st.session_state['profile']
    st.write("## User Profile")
    st.write(f"**Name:** {profile['name']}")
    st.write(f"**Special Need:** {profile['special_need']}")
else:
    st.write("No verified profile found. Please complete your profile verification.")


#MRT stations import
mrtdata = pd.read_csv("mrt_lrt_data.csv")

#Dropoff selection 
st.title('Select the station you are getting off')

#Finding station from dataset
def filter_stations(query):
    if query:
        filtered_df = df[df['station_name'].str.contains(query, case=False, na=False)]
    else:
        filtered_df = df
    return filtered_df

#App function
def main():
    st.title('MRT Cabin Status Updates')

    # Search bar
    search_query = st.text_input("Search for an MRT station:", "")

    # Filter the dataset based on the search query
    filtered_df = filter_stations(search_query)

    # Display the filtered dataset
    st.write("### Search Results")
    st.dataframe(filtered_df)


main()






















st.write('Headi')

# import data using csv
data = pd.read_csv("data.csv")
st.write(data)

# text box
x= st.text_input("Favourite Movie")
st.write(f"Your favourtie movie is: {x}")

# button
is_clicked = st.button("Click Me")

#chart
st.write("# My Cool Chart")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"]
)

st.bar_chart(chart_data)
st.line_chart(chart_data)