import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Set page configuration
st.set_page_config(page_title='Sharks Data Collection')

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from google sheets
df = conn.read(
  worksheet="Sheet1",
  ttl="5"
)

# Preprocess DataFrame: Remove empty rows/columns or replace empty cells
df.dropna(how='all', inplace=True)  # Removes rows where all cells are empty
df.dropna(axis=1, how='all', inplace=True)  # Uncomment to remove columns where all cells are empty
# df.fillna('Your Placeholder', inplace=True)  # Uncomment to replace empty cells with a placeholder

# Display content
st.markdown(' # Sharks Data Collection ')
st.dataframe(df)

st.sidebar.header("Please filter here:")
shark_name = st.sidebar.multiselect(
    "Select the Shark Name:",
    options = df['Shark_Name'].unique(),
    default = df['Shark_Name'].unique()
)
