# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 20:56:54 2021

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
    # *Dealing with missing values*
    
    It helps you deal with missing values easily without code!
    
    ---
    ''')
    
    with st.sidebar.header('Upload your CSV or excel file'):
        uploaded_file= st.sidebar.file_uploader('Upload your input csv or excel file', type=["csv","xlsx","xls"])
    if uploaded_file is not None:
        @st.cache
        def load_file():
            try:
                file1 = pd.read_excel(uploaded_file)
            except:
                file1 = pd.read_csv(uploaded_file)
            return file1
        df = load_file()
        st.write(df.head(15))
        st.write("The number of missing values in the data are as follows:")
        st.write(df.isnull().sum())
        columns= ('Delete the row', 'Fill with mean', 'Fill with median', 'Fill with mode')
        choice = st.sidebar.selectbox('How do you want to deal with missing values:', columns)
        
        if choice=='Delete the row':
            df=df.dropna()
            df=df.reset_index(drop=True)
        elif choice=='Fill with mean':
            st.write("The mean of the data is:")
            df=df.fillna(df.mean())
            df.reset_index()
        elif choice=='Fill with median':
            df=df.fillna(df.median())
            df.reset_index()
        elif choice=='Fill with mode':
            df=df.fillna(df.mode())
            df.reset_index()
            
        st.write('------------------------------------------------')    
        st.write("The number of missing values now are as follows:")
        st.write(df.isnull().sum())  
        st.write(df.head(15))
        
        file1= df.to_csv(encoding='utf-8')
        towrite = io.BytesIO()
        downloaded_file = df.to_csv(towrite,encoding='utf-8', index=False, header=True)
        towrite.seek(0)  # reset pointer
        b64 = base64.b64encode(towrite.read()).decode()  # some strings
        linko = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="anomaly.csv">Download csv file</a>'
        #linko = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file1}" download="anomaly.csv">Download csv file</a>'
        st.markdown(linko, unsafe_allow_html=True)
        
        df.to_csv("anomaly_final.csv")
