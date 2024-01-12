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
#st.dataframe(STOCKS)

STOCKS['Ticker_Index'] = STOCKS['Ticker']
STOCKS.set_index('Ticker_Index',inplace = True)

stock_dma  = STOCKS.loc[(STOCKS['50DMAModel'] == 'INVESTED') & (STOCKS['100DMAModel'] == 'INVESTED') & (STOCKS['200DMAModel'] == 'INVESTED')]
stock_tr_1 = STOCKS.loc[(STOCKS['200DMAModel'] == 'INVESTED') & (STOCKS['50DMAModel'] == 'CASH')]
stock_tr_2 = STOCKS.loc[(STOCKS['200DMAModel'] == 'CASH') & (STOCKS['50DMAModel'] == 'INVESTED') & (STOCKS['Fallin1Wmore10']<= 10)]
stock_ex_1 = STOCKS.loc[STOCKS['HistExcessReturn_12M']>=80]
stock_ex_2 = STOCKS.loc[(STOCKS['HistExcessReturn_12M']<=20) & (STOCKS['HistExcessReturn_12M'] != 0) ]
stock_vol  = STOCKS.loc[(STOCKS['HistExcessReturn_12M']<=30) & (STOCKS['Fallin1Wmore10'] >=15) & (STOCKS['HistExcessReturn_12M'] != 0)]
stock_ex50 = STOCKS.loc[(STOCKS['HistExcessReturn_12M']>=20) & (STOCKS['50DMAModel'] == 'CASH') & (STOCKS['100DMAModel'] == 'INVESTED') & (STOCKS['200DMAModel'] == 'INVESTED')]

st.header('US LARGE CAP Frame Work')

with st.sidebar:

  category = st.multiselect('Category:',STOCKS['Category'].unique())
  stock = st.multiselect('STOCK Tickers:', STOCKS['Ticker'])
  

  if (category == []) and (stock == []):

    d_stock = STOCKS.loc[STOCKS['Ticker'] == 'SPY']

  elif (category == []) and (stock != []):

    d_stock = STOCKS.loc[STOCKS['Ticker'].isin(stock)]
    stock_dma = stock_dma.loc[stock_dma['Ticker'].isin(stock)]
    stock_tr_1 = stock_tr_1.loc[stock_tr_1['Ticker'].isin(stock)]
    stock_tr_2 = stock_tr_2.loc[stock_tr_2['Ticker'].isin(stock)]
    stock_ex_1 = stock_ex_1.loc[stock_ex_1['Ticker'].isin(stock)]
    stock_ex_2 = stock_ex_2.loc[stock_ex_2['Ticker'].isin(stock)]
    stock_vol = stock_vol.loc[stock_vol['Ticker'].isin(stock)]
    stock_ex50 = stock_ex50.loc[stock_ex50['Ticker'].isin(stock)]

  elif (category != []) and (stock == []):

    d_stock = STOCKS.loc[STOCKS['Category'].isin(category)]
    stock_dma = stock_dma.loc[stock_dma['Category'].isin(category)]
    stock_tr_1 = stock_tr_1.loc[stock_tr_1['Category'].isin(category)]
    stock_tr_2 = stock_tr_2.loc[stock_tr_2['Category'].isin(category)]
    stock_ex_1 = stock_ex_1.loc[stock_ex_1['Category'].isin(category)]
    stock_ex_2 = stock_ex_2.loc[stock_ex_2['Category'].isin(category)]
    stock_vol = stock_vol.loc[stock_vol['Category'].isin(category)]
    stock_ex50 = stock_ex50.loc[stock_ex50['Category'].isin(category)]

  else:

    d_stock = STOCKS.loc[(STOCKS['Ticker'].isin(stock)) & (STOCKS['Category'].isin(category))]
    stock_dma = stock_dma.loc[(stock_dma['Ticker'].isin(stock)) & (stock_dma['Category'].isin(category))]
    stock_tr_1 = stock_tr_1.loc[(stock_tr_1['Ticker'].isin(stock)) & (stock_tr_1['Category'].isin(category))]
    stock_tr_2 = stock_tr_2.loc[(stock_tr_2['Ticker'].isin(stock)) & (stock_tr_2['Category'].isin(category))]
    stock_ex_1 = stock_ex_1.loc[(stock_ex_1['Ticker'].isin(stock)) & (stock_ex_1['Category'].isin(category))]
    stock_ex_2 = stock_ex_2.loc[(stock_ex_2['Ticker'].isin(stock)) & (stock_ex_2['Category'].isin(category))]
    stock_vol = stock_vol.loc[(stock_vol['Ticker'].isin(stock)) & (stock_vol['Category'].isin(category))]
    stock_ex50 = stock_ex50.loc[(stock_ex50['Ticker'].isin(stock)) & (stock_ex50['Category'].isin(category))]
   

  st.dataframe(d_stock[['Ticker','Name','Category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

  url = "https://drive.google.com/file/d/17ik5Xj2OBbIkau5sJtOsu9mlUFq4bFFD/view?usp=sharing"

  st.write("Click on the link to view charts(%s) " % url)

  url2 = "https://docs.google.com/spreadsheets/d/13mS_ier4GgJiqbR0ak8lgV7lWaJyY7ItWUuJH-CyEQg/edit?usp=sharing"
  
  st.write("Click on the link to view database(%s) " % url2)
  
  url3 = "https://etf-model.streamlit.app/"
  st.write("Link to the ETF Model(%s) " % url3)

st.write('## STOCKS above 50,100,200 DMA')
st.dataframe(stock_dma[['Ticker','Name','Category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('## Change in Trend')
st.write('### Above 200 DMA And Below 50 DMA')

st.dataframe(stock_tr_1[['Ticker','Name','Category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('### Below 200 DMA And Above 50 DMA')

st.dataframe(stock_tr_2[['Ticker','Name','Category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('## Excess Returns')
st.write('### Excess Return above 80 percentile')
st.dataframe(stock_ex_1[['Ticker','Name','Category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('### Excess Return below 20 percentile')
st.dataframe(stock_ex_2[['Ticker','Name','Category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('## High volatility and Large Drawdowns')
st.dataframe(stock_vol[['Ticker','Name','Category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('## Excess Returms > 20 and losing Short Term Momentum(50DMA)')
st.dataframe(stock_ex50[['Ticker','Name','Category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])
