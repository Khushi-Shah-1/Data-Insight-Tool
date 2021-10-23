# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 22:06:50 2021

@author: khushi shah
"""
import ProfilingReport
import AnomalyDetection
import RandomForest
import Plots
import MissingValue
import streamlit as st
import LinearRegression
#from footer import footer

PAGES = {"Data profiling": ProfilingReport,
         "Missing Values": MissingValue,
         "Visualization": Plots,
         "Anomaly Detector": AnomalyDetection,
         "Linear Regression": LinearRegression,
         "Random Forest Regressor": RandomForest,
         }

# Page info
st.set_page_config(
        page_title="Dive into Data",
        layout="wide",
    )


# Navigation
st.sidebar.subheader('Select the feature you want to use')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()


# footer
#footer()
