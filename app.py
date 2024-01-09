import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
  worksheet="Sheet1",
  ttl="5"
)

st.set_page_config(page_title='Sharks Data Collection')
st.markdown(' # Sharks Data Collection ')

st.dataframe(df)
