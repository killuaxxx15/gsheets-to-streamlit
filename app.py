import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
  worksheet="Sheet1",
  ttl="10"
)

# Remove columns where all values are NA.
df = df.dropna(axis=1, how='all')

# Remove rows where all values are NA.
df = df.dropna(axis=0, how='all')

# Header
st.write("Russell 1000 Growth vs. Russell 1000 Value")
st.write("\(Total Returns, 1979 - 2023\)")

# Assuming 'column_name' is the name of your column
df['Year'] = df['Year'].apply(lambda x: f'{x:.0f}')

df1 = df['Year']
st.write(df1)

# Display results in a table format.
st.dataframe(df)

df2 = conn.read(
  worksheet="Sheet2",
  ttl="10"
)

df2 = df2.dropna(axis=1, how='all')
df2 = df2.dropna(axis=0, how='all')

st.write("S&P 500, US 10-Year Treasury, and 60/40 Portfolio")
#st.table(df2)
st.dataframe(df2)
