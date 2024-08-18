import streamlit as st
import pandas as pd
import numpy as np
import datetime

"""
         
# Retail Return Manager
         
"""
dfArea = pd.read_csv('Areas.csv')
dfItem = pd.read_csv('Items.csv')

dfArea = dfArea.dropna()
dfItem = dfItem.dropna()

dfSales = pd.read_csv('SalesPredictions.csv')
dfSales['Date'] = pd.to_datetime(dfSales['Date'])
dfSales['prediction'] = dfSales['prediction'].fillna(dfSales['Qty'])
dfSales['prediction'] = dfSales['prediction'].round().astype(int)
dfSales.sort_values('Date',ascending=True)
# dfSales.set_index('Date',inplace=True)
# dfSales.info()

optArea = st.selectbox(
    'Area',
    dfArea['0'],
    index=None,
    placeholder='Select an area'
)

optItem = st.selectbox(
    'Item',
    dfItem['0'],
    index=None,
    placeholder='Select an item'
)

expdate = st.date_input('Exp Date',value=datetime.date.today(),min_value=datetime.date.today())
shelf = st.number_input('Shelf Qty',min_value=0,max_value=999,value=0)

dfAreaItemSales = dfSales[(dfSales['Area']==optArea) & 
                          (dfSales['ItemID']==optItem) & 
                          (dfSales['Set'].isin(['Train','Future'])) &
                        #   (dfSales['Date']>pd.to_datetime(datetime.date.today())) & 
                          (dfSales['Date']<pd.to_datetime(expdate))]
sales_prediction = dfAreaItemSales[(dfSales['Date']>pd.to_datetime(datetime.date.today()))]
dfAreaItemSales.set_index('Date',inplace=True)
prediction_qty = sales_prediction['prediction'].sum()
# sales_prediction
if(dfAreaItemSales.shape[0]>0):
    # dfAreaItemSales    
    'Projected Sale upto Expiry : ',prediction_qty
    if prediction_qty < shelf:
        """
        ## Recommended Return
        """
    st.line_chart(dfAreaItemSales,y=['prediction','Qty'])
else:
    'No Sales'


# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])

# st.line_chart(chart_data)