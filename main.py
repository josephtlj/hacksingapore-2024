import streamlit as st
import pandas as pd
import numpy as np

st.title('🎈 Prototype')

st.link_button("Profile", "http://localhost:8501/profile")

st.write('Heading 1')

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