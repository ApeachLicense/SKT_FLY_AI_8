import pandas as pd
import streamlit as st

df = pd.DataFrame({
    'First Column': [1, 2, 3, 4],
    'Second Column': [10, 20, 30, 40]
})

st.write("# I am a king of the world!")
st.write(df)