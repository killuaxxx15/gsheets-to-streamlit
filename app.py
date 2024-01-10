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
#st.dataframe(df)

st.sidebar.header("Please filter here:")
shark_name = st.sidebar.multiselect(
    "Select the Shark Name:",
    options = df['Shark_Name'].unique(),
    default = df['Shark_Name'].unique()
)

df_selection = df.query(
    "Shark_Name == @shark_name"
)

st.dataframe(df_selection)



### SHEET 2

# Read data from google sheets
df2 = conn.read(
  worksheet="Sheet2",
  ttl="5"
)

# Preprocess DataFrame: Remove empty rows/columns or replace empty cells
df2.dropna(how='all', inplace=True)  # Removes rows where all cells are empty
df2.dropna(axis=1, how='all', inplace=True)  # Uncomment to remove columns where all cells are empty

st.markdown(" # Original ")
st.dataframe(df2)

# Function to create a colored circle based on value
def colored_circle(value):
    color = "red" if value < 1 else "green"
    return f'<span style="height: 15px; width: 15px; background-color: {color}; border-radius: 50%; display: inline-block;"></span>'

# Apply the colored circle function to your specific column
df2['Colored_Circle'] = df2['Column_C'].apply(colored_circle)

# Display the DataFrame
st.write(df2.to_html(escape=False), unsafe_allow_html=True)
