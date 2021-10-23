# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 19:22:37 2021

@author: khushi shah
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def app():
    
    with st.sidebar.header('Upload your CSV or excel file'):
        uploaded_file= st.sidebar.file_uploader('Upload your input csv or excel file', type=["csv","xlsx","xls"])
    
    # Model building
    def build_model(df):
        X = df.iloc[:,:-1] # Using all column except for the last column as X
        Y = df.iloc[:,-1] # Selecting the last column as Y
    
        # Data splitting
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=(100-split_size)/100)
        
        st.markdown('**1.2. Data splits**')
        st.write('Training set')
        st.info(X_train.shape)
        st.write('Test set')
        st.info(X_test.shape)
    
        st.markdown('**1.3. Variable details**:')
        st.write('X variable')
        st.info(list(X.columns))
        st.write('Y variable')
        st.info(Y.name)
    
        lr = LinearRegression(
            random_state=parameter_random_state,   
            criterion=parameter_criterion,
            bootstrap=parameter_bootstrap,
            oob_score=parameter_oob_score,
            n_jobs=parameter_n_jobs)
        lr.fit(X_train, Y_train)
    
        st.subheader('2. Model Performance')
    
        st.markdown('**2.1. Training set**')
        Y_pred_train = lr.predict(X_train)
        st.write('Coefficient of determination ($R^2$):')
        st.info( r2_score(Y_train, Y_pred_train) )
    
        st.write('Error (MSE or MAE):')
        st.info( mean_squared_error(Y_train, Y_pred_train) )
    
        st.markdown('**2.2. Test set**')
        Y_pred_test = lr.predict(X_test)
        st.write('Coefficient of determination ($R^2$):')
        st.info( r2_score(Y_test, Y_pred_test) )
    
        st.write('Error (MSE or MAE):')
        st.info( mean_squared_error(Y_test, Y_pred_test) )
    
        st.subheader('3. Model Parameters')
        st.write(lr.get_params())
    
    #---------------------------------#
    st.write("""
    # Linear Regression

    Try adjusting the hyperparameters!    
    """)
    
    #---------------------------------#
    
    # Sidebar - Specify parameter settings
    with st.sidebar.header('2. Set Parameters'):
        split_size = st.sidebar.slider('Data split ratio (% for Training Set)', 10, 90, 80, 5)
    
    
    with st.sidebar.subheader('2.2. General Parameters'):
        parameter_random_state = st.sidebar.slider('Seed number (random_state)', 0, 1000, 42, 1)
        parameter_criterion = st.sidebar.select_slider('Performance measure (criterion)', options=['mse', 'mae'])
        parameter_bootstrap = st.sidebar.select_slider('Bootstrap samples when building trees (bootstrap)', options=[True, False])
        parameter_oob_score = st.sidebar.select_slider('Whether to use out-of-bag samples to estimate the R^2 on unseen data (oob_score)', options=[False, True])
        parameter_n_jobs = st.sidebar.select_slider('Number of jobs to run in parallel (n_jobs)', options=[1, -1])
    
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.markdown('**1.1. Glimpse of dataset**')
        st.write(df)
        build_model(df)
    else:
        st.info('Awaiting for CSV file to be uploaded.')
        if st.button('Press to use Example Dataset'):
            def load_data():
                a = pd.DataFrame(
                    np.random.rand(100, 4),
                    columns=['a', 'b', 'c', 'd']
                )
                return a
            df = load_data()
            st.write(df.head(5))
            build_model(df)
