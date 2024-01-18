import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from Google Sheets
ETFs = conn.read(
  worksheet="STOCK_DATA",
  ttl="5",
)

# Convert the data to a DataFrame if necessary
#STOCKS = pd.DataFrame(STOCKS)
#tickers = STOCKS['Ticker']
#st.dataframe(STOCKS)

ETFs['Ticker_Index'] = ETFs['Ticker']
ETFs.set_index('Ticker_Index',inplace = True)


etf_dma = ETFs[['Ticker','Name','Category','Sub category','Price','50DMAModel','100DMAModel','200DMAModel']]
etf_dma['>50DMA'] = (etf_dma['50DMAModel'] == "INVESTED").astype(int)
etf_dma['>200DMA'] = (etf_dma['200DMAModel'] == "INVESTED").astype(int)
etf_dma['>50DMA>200DMA'] = (etf_dma['200DMAModel'] == "INVESTED").astype(int)
etf_dma['SCORE'] = etf_dma['>50DMA'] + etf_dma['>200DMA'] + etf_dma['>50DMA>200DMA']
etf_dma = etf_dma[['Ticker','Name','Category','Sub category','Price','>50DMA','>50DMA>200DMA','>200DMA','SCORE']]


etf_tr_1 = ETFs.loc[(ETFs['200DMAModel'] == 'INVESTED') & (ETFs['50DMAModel'] == 'CASH')]
etf_tr_2 = ETFs.loc[(ETFs['200DMAModel'] == 'CASH') & (ETFs['50DMAModel'] == 'INVESTED') & (ETFs['Fallin1Wmore10']<= 10)]
etf_ex_1 = ETFs.loc[ETFs['HistExcessReturn_12M']>=80]
etf_ex_2 = ETFs.loc[(ETFs['HistExcessReturn_12M']<=20) & (ETFs['HistExcessReturn_12M'] != 0) ]
etf_vol  = ETFs.loc[(ETFs['HistExcessReturn_12M']<=30) & (ETFs['Fallin1Wmore10'] >=15) & (ETFs['HistExcessReturn_12M'] != 0)]
etf_ex50 = ETFs.loc[(ETFs['HistExcessReturn_12M']>=20) & (ETFs['50DMAModel'] == 'CASH') & (ETFs['100DMAModel'] == 'INVESTED') & (ETFs['200DMAModel'] == 'INVESTED')]

st.header('India Charts')

with st.sidebar:

  category = st.multiselect('Category:',ETFs['Category'].unique())
  sub = st.multiselect ('Sub Category:',ETFs['Sub category'].unique())
  etf = st.multiselect('ETF Tickers:', ETFs['Ticker'])
  

  if (category == []) and (etf == []) and (sub ==[]):

    d_etf = ETFs.loc[ETFs['Ticker'] == '^NSEI']

  elif (category == []) and (etf == []) and (sub !=[]):

    d_etf = ETFs.loc[ETFs['Sub category'].isin(sub)]
    etf_dma = etf_dma.loc[etf_dma['Sub category'].isin(sub)]
    etf_tr_1 = etf_tr_1.loc[etf_tr_1['Sub category'].isin(sub)]
    etf_tr_2 = etf_tr_2.loc[etf_tr_2['Sub category'].isin(sub)]
    etf_ex_1 = etf_ex_1.loc[etf_ex_1['Sub category'].isin(sub)]
    etf_ex_2 = etf_ex_2.loc[etf_ex_2['Sub category'].isin(sub)]
    etf_ex50 = etf_ex50.loc[etf_ex50['Sub category'].isin(sub)]

  elif (category == []) and (etf != []) and (sub ==[]):

    d_etf = ETFs.loc[ETFs['Ticker'].isin(etf)]
    etf_dma = etf_dma.loc[etf_dma['Ticker'].isin(etf)]
    etf_tr_1 = etf_tr_1.loc[etf_tr_1['Ticker'].isin(etf)]
    etf_tr_2 = etf_tr_2.loc[etf_tr_2['Ticker'].isin(etf)]
    etf_ex_1 = etf_ex_1.loc[etf_ex_1['Ticker'].isin(etf)]
    etf_ex_2 = etf_ex_2.loc[etf_ex_2['Ticker'].isin(etf)]
    etf_vol = etf_vol.loc[etf_vol['Ticker'].isin(etf)]
    etf_vol = etf_vol.loc[etf_vol['Ticker'].isin(etf)]
    etf_ex50 = etf_ex50.loc[etf_ex50['Ticker'].isin(etf)]

  elif (category == []) and (etf != []) and (sub !=[]):
    
    d_etf = ETFs.loc[(ETFs['Ticker'].isin(etf)) & (ETFs['Sub category'].isin(sub))]
    etf_dma = etf_dma.loc[(etf_dma['Ticker'].isin(etf)) & (etf_dma['Sub category'].isin(sub))]
    etf_tr_1 = etf_tr_1.loc[(etf_tr_1['Ticker'].isin(etf)) & (etf_tr_1['Sub category'].isin(sub))]
    etf_tr_2 = etf_tr_2.loc[(etf_tr_2['Ticker'].isin(etf)) & (etf_tr_2['Sub category'].isin(sub))]
    etf_ex_1 = etf_ex_1.loc[(etf_ex_1['Ticker'].isin(etf)) & (etf_ex_1['Sub category'].isin(sub))]
    etf_ex_2 = etf_ex_2.loc[(etf_ex_2['Ticker'].isin(etf)) & (etf_ex_2['Sub category'].isin(sub))]
    etf_vol = etf_vol.loc[(etf_vol['Ticker'].isin(etf)) & (etf_vol['Sub category'].isin(sub))]
    etf_ex50 = etf_ex50.loc[(etf_ex50['Ticker'].isin(etf)) & (etf_ex50['Sub category'].isin(sub))]


  elif (category != []) and (etf == []) and (sub ==[]):

    d_etf = ETFs.loc[ETFs['Category'].isin(category)]
    etf_dma = etf_dma.loc[etf_dma['Category'].isin(category)]
    etf_tr_1 = etf_tr_1.loc[etf_tr_1['Category'].isin(category)]
    etf_tr_2 = etf_tr_2.loc[etf_tr_2['Category'].isin(category)]
    etf_ex_1 = etf_ex_1.loc[etf_ex_1['Category'].isin(category)]
    etf_ex_2 = etf_ex_2.loc[etf_ex_2['Category'].isin(category)]
    etf_vol = etf_vol.loc[etf_vol['Category'].isin(category)]
    etf_ex50 = etf_ex50.loc[etf_ex50['Category'].isin(category)]

  elif (category != []) and (etf == []) and (sub !=[]):

    d_etf = ETFs.loc[(ETFs['Category'].isin(category)) & (ETFs['Sub category'].isin(sub))]
    etf_dma = etf_dma.loc[(etf_dma['Category'].isin(category)) & (etf_dma['Sub category'].isin(sub))]
    etf_tr_1 = etf_tr_1.loc[(etf_tr_1['Category'].isin(category)) & (etf_tr_1['Sub category'].isin(sub))]
    etf_tr_2 = etf_tr_2.loc[(etf_tr_2['Category'].isin(category)) & (etf_tr_2['Sub category'].isin(sub))]
    etf_ex_1 = etf_ex_1.loc[(etf_ex_1['Category'].isin(category)) & (etf_ex_1['Sub category'].isin(sub))]
    etf_ex_2 = etf_ex_2.loc[(etf_ex_2['Category'].isin(category)) & (etf_ex_2['Sub category'].isin(sub))]
    etf_vol = etf_vol.loc[(etf_vol['Category'].isin(category)) & (etf_vol['Sub category'].isin(sub))]
    etf_ex50 = etf_ex50.loc[(etf_ex50['Category'].isin(category)) & (etf_ex50['Sub category'].isin(sub))]

  elif (category  != []) and (etf != []) and (sub ==[]):

    d_etf = ETFs.loc[(ETFs['Ticker'].isin(etf)) & (ETFs['Category'].isin(category))]
    etf_dma = etf_dma.loc[(etf_dma['Ticker'].isin(etf)) & (etf_dma['Category'].isin(category))]
    etf_tr_1 = etf_tr_1.loc[(etf_tr_1['Ticker'].isin(etf)) & (etf_tr_1['Category'].isin(category))]
    etf_tr_2 = etf_tr_2.loc[(etf_tr_2['Ticker'].isin(etf)) & (etf_tr_2['Category'].isin(category))]
    etf_ex_1 = etf_ex_1.loc[(etf_ex_1['Ticker'].isin(etf)) & (etf_ex_1['Category'].isin(category))]
    etf_ex_2 = etf_ex_2.loc[(etf_ex_2['Ticker'].isin(etf)) & (etf_ex_2['Category'].isin(category))]
    etf_vol = etf_vol.loc[(etf_vol['Ticker'].isin(etf)) & (etf_vol['Category'].isin(category))]
    etf_ex50 = etf_ex50.loc[(etf_ex50['Ticker'].isin(etf)) & (etf_ex50['Category'].isin(category))]

  else:

    d_etf = ETFs.loc[(ETFs['Ticker'].isin(etf)) & (ETFs['Category'].isin(category)) & (ETFs['Sub category'].isin(sub))]
    etf_dma = etf_dma.loc[(etf_dma['Ticker'].isin(etf)) & (etf_dma['Category'].isin(category)) & (etf_dma['Sub category'].isin(sub))]
    etf_tr_1 = etf_tr_1.loc[(etf_tr_1['Ticker'].isin(etf)) & (etf_tr_1['Category'].isin(category)) & (etf_tr_1['Sub category'].isin(sub))]
    etf_tr_2 = etf_tr_2.loc[(etf_tr_2['Ticker'].isin(etf)) & (etf_tr_2['Category'].isin(category)) & (etf_tr_2['Sub category'].isin(sub))]
    etf_ex_1 = etf_ex_1.loc[(etf_ex_1['Ticker'].isin(etf)) & (etf_ex_1['Category'].isin(category)) & (etf_ex_1['Sub category'].isin(sub))]
    etf_ex_2 = etf_ex_2.loc[(etf_ex_2['Ticker'].isin(etf)) & (etf_ex_2['Category'].isin(category)) & (etf_ex_2['Sub category'].isin(sub))]
    etf_vol = etf_vol.loc[(etf_vol['Ticker'].isin(etf)) & (etf_vol['Category'].isin(category)) & (etf_vol['Sub category'].isin(sub))]
    etf_ex50 = etf_ex50.loc[(etf_ex50['Ticker'].isin(etf)) & (etf_ex50['Category'].isin(category)) & (etf_ex50['Sub category'].isin(sub))]
   

  st.dataframe(d_etf[['Ticker','Name','Category','Sub category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

  url = "https://drive.google.com/file/d/1V60lDnSXZrDjUV9yE-si-8nRRADsWwkc/view?usp=sharing"

  st.write("Click on the link to view charts(%s) " % url)

  url2 = "https://docs.google.com/spreadsheets/d/109_ONvn6OUlDksO7B6-Wrq6klmDkbIUH5AscqLJmhX8/edit#gid=138664075"
  
  st.write("Click on the link to view database(%s) " % url2)
  
  url3 = "https://us-stock-model.streamlit.app/"
  st.write("Link to the US Stock Model(%s) " % url3)


st.write('## 50 & 200 MA Signals')
st.dataframe(etf_dma[['Ticker','Name','Category','Sub category','Price','SCORE','>50DMA','>50DMA>200DMA','>200DMA']])

st.write('## Change in Trend')
st.write('### Change in Trend - Negative')

st.dataframe(etf_tr_1[['Ticker','Name','Category','Sub category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('### Change in Trend - Positive')

st.dataframe(etf_tr_2[['Ticker','Name','Category','Sub category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('## Excess Returns')
st.write('### Excess Return above 80 percentile')
st.dataframe(etf_ex_1[['Ticker','Name','Category','Sub category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('### Excess Return below 20 percentile')
st.dataframe(etf_ex_2[['Ticker','Name','Category','Sub category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('## High volatility and Large Drawdowns')
st.dataframe(etf_vol[['Ticker','Name','Category','Sub category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])

st.write('## Excess Returns > 20 and losing Short Term Momentum(50DMA)')
st.dataframe(etf_ex50[['Ticker','Name','Category','Sub category','Price','PctRank_1M','PctRank_3M','PctRank_6M','PctRank_12M','HistExcessReturn_1M','HistExcessReturn_3M','HistExcessReturn_6M','HistExcessReturn_12M','ChgRnk_1M','ChgRnk_3M','ChgRnk_6M','ChgRnk_12M']])
