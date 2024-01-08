import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
  worksheet="Sheet1",
  ttl="10m"
)

# Remove columns where all values are NA.
df = df.dropna(axis=1, how='all')

# Remove rows where all values are NA.
df = df.dropna(axis=0, how='all')

# Header
st.header("Table 1")

# Display results in a table format.
st.dataframe(df)

df2 = conn.read(
  worksheet="Sheet2",
  ttl="10m"
)

df2 = df2.dropna(axis=1, how='all')
df2 = df2.dropna(axis=0, how='all')

st.header("Table 2")
#st.table(df2)
st.dataframe(df2)
