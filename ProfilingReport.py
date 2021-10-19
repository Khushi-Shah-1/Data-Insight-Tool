import numpy as np
import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

def app():

    st.markdown('''
    # *Data Profiling*
    
    It helps you analyze your data effectively without code!
    
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
        pr= ProfileReport(df, explorative=True)
        st.header('**Input Dataframe**')
        st.write(df)
        st.write('---')
        st.header('** Pandas profiling report **')
        st_profile_report(pr)
    else:
        st.info('Awaiting for CSV file to be uploaded.')
        if st.button('Press to use Example Dataset'):
            @st.cache
            def load_data():
                a = pd.DataFrame(
                    np.random.rand(100, 4),
                    columns=['a', 'b', 'c', 'd']
                )
                return a
            df = load_data()
            pr = ProfileReport(df, explorative=True)
            st.header('**Input DataFrame**')
            st.write(df)
            st.write('---')
            st.header('**Pandas Profiling Report**')
            st_profile_report(pr)
    
    
    
    
    
    
    
