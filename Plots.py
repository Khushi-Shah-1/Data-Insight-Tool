# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 18:30:58 2021

@author: khushi shah
"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import altair as alt
import plotly.figure_factory as ff
import plotly.express as px

def app():
    
    st.markdown('''
    # *Data Visualization*
    
    It helps you visualize your data effectively without code!
    
    ---
    ''')
    
    with st.sidebar.header('Upload your CSV or excel file'):
        uploaded_file= st.sidebar.file_uploader('Upload your input csv or excel file', type=["csv","xlsx","xls"])
    
    def make_chart(df):
        columns = df.columns.tolist()
        first = st.sidebar.selectbox('Select your first variable:', columns) 
        
        charts= ('Line chart', 'Bar plot','Scatter Plot', 'Pie Chart','Histogram', 'Box Plot','Violin Plot')
        graph = st.sidebar.selectbox('Select the type of chart you want to see:', charts)
        
        if graph=='Line chart':
            second = st.sidebar.selectbox('Select your second variable:', columns) 
            fig = px.line(df, x=first, y=second, template = 'plotly_dark')                    
            st.plotly_chart(fig)
        elif graph=='Bar plot':
            second = st.sidebar.selectbox('Select your second variable:', columns) 
            fig = px.bar(df, x=first, y=second, template = 'plotly_dark')
            st.plotly_chart(fig)
        elif graph=='Scatter Plot':
            second = st.sidebar.selectbox('Select your second variable:', columns) 
            fig = px.scatter(df, x=first, y=second, template = 'plotly_dark')
            st.plotly_chart(fig)
        elif graph=='Pie Chart':
            second = st.sidebar.selectbox('Select your second variable:', columns) 
            fig = px.pie(df, values=first, names=second, template = 'plotly_dark')
            st.plotly_chart(fig)
        elif graph=='Histogram':
            fig = px.histogram(df, x=first, template = 'plotly_dark')
            st.plotly_chart(fig)
        elif graph=='Box Plot':
            fig = px.box(df, x=first, template = 'plotly_dark')
            st.plotly_chart(fig)
        elif graph=='Violin Plot':
            fig = px.violin(df, x=first, template = 'plotly_dark')
            st.plotly_chart(fig)
    
   
    if uploaded_file is not None:
        @st.cache
        def load_csv():
            try:
                csv = pd.read_excel(uploaded_file)
            except:
                csv = pd.read_csv(uploaded_file)
            return csv
        df = load_csv() 
        make_chart(df)
        st.markdown('**1.1. Glimpse of dataset**')
        st.write(df)
    
    else:
        st.info('Awaiting for CSV file to be uploaded.')
        if st.button('Press to use Example Dataset'):
            # Example data
            def load_data():
                a = pd.DataFrame(
                    np.random.rand(100, 4),
                    columns=['a', 'b', 'c', 'd']
                )
                return a
            df = load_data()
            make_chart(df)
            st.markdown('**1.1. Glimpse of dataset**')
            st.write(df)