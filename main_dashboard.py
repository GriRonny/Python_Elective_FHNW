import streamlit as st
import pandas as pd
import numpy as np
import customer_scenario
import sales_scenario
import market_scenario

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="centered", initial_sidebar_state="expanded")


# this method just loads the csv file we upload using Pandas
def load_csv(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        st.error("Something went wrong")
        return None


# Initialize session state
# 'View is are session_state object name, and we assign the default value 'upload' at the beginning
if 'view' not in st.session_state:
    st.session_state.view = 'upload'  # Create default view


# Function to switch view
def switch_view(view_name):
    st.session_state.view = view_name  # Create view according to passed parameter
    st.rerun()  # Trigger rerun everytime function is called to update view accordingly.


if st.session_state.view == 'upload':  # Display the "Upload" view if the session state == "upload"

    st.header("Welcome to our data our dashboard :sunglasses:")

    st.write("First, select the latest global_superstore.csv file. \n"
             "\nNext, enjoy our dashboard that we created!:fire:")

    uploaded_csv = st.file_uploader("Choose a CSV file to be processed.", type="csv")

    if uploaded_csv is not None:
        df = load_csv(uploaded_csv)
        if df is not None:
            st.session_state.df = df  # Store dataframe in session state
            st.success("CSV file successfully loaded!")
            st.write(df)
            if st.button("Start analysing!"):
                switch_view('analysis')  # Call function to create "analysis" view and update view
        else:
            st.error("Failed to load CSV file.")
    else:
        st.info("Please upload a CSV file.")

elif st.session_state.view == 'analysis':  # Here we display the "Upload" view if the session state == "analysis"
    st.header("Choose what you want to analyse!")
    st.write("Below are the different analyses.")

    # Create three parallel sections
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Customer Behaviour")
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in.")
        if st.button("Button 1"):
            st.write("Button 1 clicked")
            switch_view('customer')

    with col2:
        st.subheader("Section 2")
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in.")
        if st.button("Button 2"):
            st.write("Button 2 clicked")
            switch_view('market')

    with col3:
        st.subheader("Section 3")
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in.")
        if st.button("Button 3"):
            st.write("Button 3 clicked")
            switch_view('sales')

    if st.button("Go back to Upload"):  # If this button is pressed, the user returns to the defined view.
        switch_view('upload')  # switch_view function called with parameter "upload"

elif st.session_state.view == 'customer':  # Here we display the "Upload" view if the session state == "customer"

    customer_scenario.CustomerScenario().customer_logic()  # Call customer logic method from CustomerScenario class

elif st.session_state.view == 'market':

    market_scenario.MarketScenario().market_logic()

elif st.session_state.view == 'sales':

    sales_scenario.SalesScenario().sales_logic()
