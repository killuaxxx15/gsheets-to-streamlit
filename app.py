import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from Google Sheets
STOCKS = conn.read(
  worksheet="STOCK_DATA",
  ttl="5",
)

# Convert the data to a DataFrame if necessary
#STOCKS = pd.DataFrame(STOCKS)
#tickers = STOCKS['Ticker']
st.dataframe(STOCKS)
