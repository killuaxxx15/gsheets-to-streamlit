import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

spreadsheet_id = "109_ONvn6OUlDksO7B6-Wrq6klmDkbIUH5AscqLJmhX8"  # Replace with your actual spreadsheet ID
connection_name = "my_gsheet_connection"     # You can choose any name you like
conn = GSheetsConnection(spreadsheet_id=spreadsheet_id, connection_name=connection_name)

# Read the data from the Google Sheet.
df = conn.read(
  spreadsheet_id=spreadsheet_id,
  worksheet="Sheet1",
  ttl="10m"
)

# Function to convert percentage strings to float.
def convert_percentage(val):
    if isinstance(val, str) and '%' in val:
        return float(val.replace('%', '')) / 100
    return val

# Apply the function to convert percentages and cast 'Year' column to integers.
df = df.applymap(convert_percentage)
try:
    df['Year'] = df['Year'].astype(int)
except KeyError:
    st.error("Column 'Year' not found in the data.")
except ValueError:
    st.error("Non-numeric values found in 'Year' column, cannot convert to integers.")

# Remove columns where all values are NA.
df = df.dropna(axis=1, how='all')

# Remove rows where all values are NA.
df = df.dropna(axis=0, how='all')

# Header
st.header("Table 1")

# Display results in a table format.
st.table(df)
