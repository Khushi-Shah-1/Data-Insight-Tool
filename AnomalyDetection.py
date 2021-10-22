# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 22:34:17 2021

@author: khushi shah
"""
import pandas as pd
import streamlit as st
from pycaret.anomaly import *
import plotly.graph_objects as go
import altair as alt
import plotly.figure_factory as ff
import plotly.express as px
import io
import os
import base64

def app():

    st.markdown('''
    # *Anomaly detection*
    
    It helps you to find outliers in the dataset. It can only be used for regression problems.
    
    ---
    ''')

    # Upload CSV data
    with st.sidebar.header('Upload your CSV or excel data'):
        uploaded_file = st.sidebar.file_uploader("Upload your input CSV or excel file", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        @st.cache
        def load_csv():
            try:
                csv = pd.read_excel(uploaded_file)
            except:
                csv = pd.read_csv(uploaded_file)
            return csv
        df = load_csv()
        st.header('**Input Dataframe**')
        st.write(df.sample(10))
        
        # target column selection
        df = df.select_dtypes('number')
        columns = df.columns.tolist()
        target_column = st.sidebar.selectbox('Select your target column:', columns)
        
        # shortlist column based on correlation with target
        corr = df.corr()
        cor_target = abs(corr[target_column])
        relevan_cols = cor_target[cor_target>=0.2].index
        df = df[relevan_cols]
    
        # Anomaly detection using Isolation forest model

        s = setup(df, session_id=123, silent=True)
        iforest = create_model('iforest', fraction=0.01)
        iforest_results = assign_model(iforest)
        anomaly = iforest_results[iforest_results['Anomaly'] == 1]
        #anomaly = anomaly.drop('Anomaly', axis=1)
        st.write('---')
        st.header('**Data contains Anomaly**')
        st.write(anomaly.head(10))
        st.text(f"Total {anomaly.shape[0]} anomalies found")
        outlier_dates = iforest_results[iforest_results['Anomaly'] == 1].index
        # obtain y value of anomalies to plot
        y_values = [iforest_results.loc[i][target_column] for i in outlier_dates]
         
        # plot value on y-axis and date on x-axis
        fig = px.line(iforest_results, x=iforest_results.index, y=target_column, title='ANOMALY DETECTION', template = 'plotly_dark')
        # create list of outlier_dates
        outlier_dates = iforest_results[iforest_results['Anomaly'] == 1].index
        # obtain y value of anomalies to plot
        y_values = [iforest_results.loc[i][target_column] for i in outlier_dates]
        fig.add_trace(go.Scatter(x=outlier_dates, y=y_values, mode = 'markers', 
                        name = 'Anomaly', 
                        marker=dict(color='red',size=10)))
                
        st.plotly_chart(fig)
        
        
        towrite = io.BytesIO()
        downloaded_file = anomaly.to_excel(towrite, encoding='utf-8', index=False, header=True)
        towrite.seek(0)  # reset pointer
        b64 = base64.b64encode(towrite.read()).decode()  # some strings
        linko = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="anomaly.xlsx">Download excel file</a>'
        st.markdown(linko, unsafe_allow_html=True)

    
    else:
        st.info('Awaiting for CSV file to be uploaded.')
        if st.button('Press to use Example Dataset'):
            # Example data
            @st.cache
            def load_data():
                a = pd.DataFrame(
                    np.random.rand(100, 4),
                    columns=['a', 'b', 'c', 'd']
                )
                return a
            df = load_data()
            s = setup(df, session_id=123, silent=True)
            iforest = create_model('iforest', fraction=0.1)
            iforest_results = assign_model(iforest)
            anomaly = iforest_results[iforest_results['Anomaly'] == 1]
            st.header('**Input DataFrame**')
            st.write(df)
            st.write('---')
            st.header('**Data contains Anomaly**')
            st.write(anomaly.head(10))
        
