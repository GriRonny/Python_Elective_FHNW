import streamlit as st
import pandas as pd
import numpy as np
import customer_scenario
import sales_scenario
import market_scenario


st.set_page_config(page_title="Business Dashboard", page_icon="📊", layout="centered", initial_sidebar_state="expanded")


# Initialize session state
if 'view' not in st.session_state:
    st.session_state.view = 'upload'  # Create default view


# Function to switch view
def switch_view(view_name):
    st.session_state.view = view_name  # Create view according to passed parameter
    st.rerun()  # Trigger rerun everytime function is called to update view accordingly.


st.session_state.switch_view = switch_view  # Make switch_view function accessible from outside

if st.session_state.view == 'upload':  # Display the "Upload" view if the session state == "upload"

    st.header("Upload CSV file")

    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
             "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
             "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
             "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in.")

    # Define required columns as a constant variable
    REQUIRED_COLUMNS = [
        "Order Date", "Ship Date", "Ship Mode", "Customer Name", "Customer DOB", "Segment", "City", "State", "Country",
        "Postal Code", "Market", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Sales",
        "Quantity",
        "Discount", "Profit", "Shipping Cost", "Order Priority", "Payment Method"
    ]

    def load_csv(file):
        try:
            df_check = pd.read_csv(file)

            # Check if each required column is in file. If not, add it to this list.
            missing_columns = [col for col in REQUIRED_COLUMNS if col not in df_check.columns]
            if missing_columns:
                st.error(f"Missing columns: {', '.join(missing_columns)}. Please check your .csv file.")
                return None
            else:
                return df_check

        except Exception as e:
            st.error("Something went wrong while uploading your file.")
            print(f"Error loading CSV file: {e}")
            return None

    uploaded_csv = st.file_uploader("Choose a CSV file to be processed.", type="csv")

    if uploaded_csv is not None:
        df = load_csv(uploaded_csv)  # Call load_csv method with .csv from file uploader as parameter
        if df is not None:
            st.session_state.df = df  # Store dataframe in session state
            st.success("CSV file successfully loaded!")
            st.write(df)
            if st.button("Proceed to Analysis"):
                switch_view('analysis')  # Call function to create "analysis" view and update view
        else:
            st.error("Failed to load CSV file.")
    else:
        st.info("Please upload a CSV file.")

elif st.session_state.view == 'analysis':  # Here we display the "Upload" view if the session state == "analysis"
    st.header("Choose desired analysis scope")
    st.write("This is the analysis view.")

    # Create three parallel sections
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Section 1")
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

    customer_scenario.CustomerScenario().customer_logic() # Call customer logic method from CustomerScenario class

elif st.session_state.view == 'market':

    market_scenario.MarketScenario().market_logic()

elif st.session_state.view == 'sales':

    sales_scenario.SalesScenario().sales_logic()
