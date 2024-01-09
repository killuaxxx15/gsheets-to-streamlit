import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Set page configuration
st.set_page_config(page_title='Sharks Data Collection')

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
  worksheet="Sheet1",
  ttl="5"
)

# Display content
st.markdown(' # Sharks Data Collection ')
st.dataframe(df)
