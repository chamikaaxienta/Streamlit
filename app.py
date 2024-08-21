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

dfPrediction = dfSales[(dfSales['Date']>pd.to_datetime('2024-01-01'))]

st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)
def header(url,warning):
     if(warning):
         st.markdown(f'<p style="background-color:#D22B2B;color:#ffffff;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)
     else:
        st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)



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

col1, col2 = st.columns(2)
with col1:
    btnSubmit = st.button('Submit')
with col2:
    btnClear = st.button('Clear')

if(btnSubmit):
    # sales_prediction dfPrediction
    if(optArea!=None and optItem!=None):
        # dfAreaItemSales = dfSales[(dfSales['Area']==optArea) & 
        #                   (dfSales['ItemID']==optItem) & 
        #                 #   (dfSales['Date']>=pd.to_datetime(datetime.date.today().replace(datetime.date.today().month-5).replace(day=1))) &
        #                   (dfSales['Set'].isin(['Train','Future'])) &
        #                 #   (dfSales['Date']>pd.to_datetime(datetime.date.today())) & 
        #                   (dfSales['Date']<pd.to_datetime(expdate))]
        dfAreaItemSales = dfPrediction[(dfPrediction['Area']==optArea) & 
                          (dfPrediction['ItemID']==optItem) & 
                          (dfPrediction['Set'].isin(['Train','Future'])) &
                          (dfPrediction['Date']<pd.to_datetime(expdate))]
        sales_prediction = dfAreaItemSales[(dfSales['Date']>pd.to_datetime(datetime.date.today()))]
        dfAreaItemSales.set_index('Date',inplace=True)
        prediction_qty = sales_prediction['prediction'].sum()
        
        if(dfAreaItemSales.shape[0]>0):  
            header('Projected Sale upto Expiry : '+str(prediction_qty),False)            
            if prediction_qty < shelf:
                header('Recommended Return',True) 
            st.line_chart(dfAreaItemSales,y=['prediction','Qty'])           
        else:
            header('No Sales',False)
