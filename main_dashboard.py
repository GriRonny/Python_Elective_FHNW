import streamlit as st
import pandas as pd
import customer_scenario
import sales_scenario
import market_scenario
import profitability_scenario
import product_scenario
import json
import time
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Business Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# Load Lottie animation
def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

# Polarbear Lotti
lottie_polar_bear = load_lottiefile("polarbear.json")

# Initialize session state
if 'view' not in st.session_state:
    st.session_state.view = 'upload'  # Create default view

# Function to switch view
def switch_view(view_name):
    st.session_state.view = view_name  # Create view according to passed parameter
    st.rerun()  # Trigger rerun every time function is called to update view accordingly.

st.session_state.switch_view = switch_view  # Make switch_view function accessible from outside

if st.session_state.view == 'upload':  # Display the "Upload" view if the session state == "upload"
    # Center the "Welcome" text
    empty_col1, centered_col, empty_col2 = st.columns([1, 2, 1])
    with centered_col:
        st.markdown("## *Welcome* to Your Business Dashboard 📊")

    # Center the rest of the header text
    empty_col1, centered_col, empty_col2 = st.columns([1, 2, 1])
    with centered_col:
        st.markdown("### Get Started with Your Business Insights!")

        st.write("")

    empty_col1, col1, welcome_col, col2, empty_col2 = st.columns([1, 2, 0.01, 2, 1])
    with col1:
        st_lottie(lottie_polar_bear, height=400, key="polar_bear")

    with col2:
        st.markdown("#### Start by uploading your data file")
        st.write("To upload your data file, please follow these steps:")
        st.write("1. Select the latest `global_superstore.csv` file.")
        st.write("2. Drag and drop the file into the area below or click 'Browse files' to select it.")
        st.write("3. Click 'Start Analysing' to begin your data insights journey.")

        # Define required columns as a constant variable
        REQUIRED_COLUMNS = [
            "Order Date", "Ship Date", "Ship Mode", "Customer Name", "Customer DOB", "Segment", "City", "State", "Country",
            "Postal Code", "Market", "Region", "Product ID", "Category", "Sub-Category", "Product Name", "Sales",
            "Quantity", "Discount", "Profit", "Shipping Cost", "Order Priority", "Payment Method"
        ]

        uploaded_csv = st.file_uploader("Drag and drop file here", type="csv")

        def load_csv(file):
            try:
                df_check = pd.read_csv(file)

                # Check if each required column is in file. If not, add it to this list.
                missing_columns = [col for col in REQUIRED_COLUMNS if col not in df_check.columns]
                if missing_columns:
                    st.error(f"Missing columns: {', '.join(missing_columns)}. Please check your CSV file.")
                    return None
                else:
                    return df_check

            except Exception as e:
                st.error("Something went wrong while uploading your file.")
                print(f"Error loading CSV file: {e}")
                return None

        if uploaded_csv is not None:
            with st.spinner("Processing file..."):
                time.sleep(1)  # Simulate a delay for processing
            df = load_csv(uploaded_csv)
            if df is not None:
                st.session_state.df = df  # Store dataframe in session state
                st.success("CSV file successfully uploaded!")
                st.write(df)
                if st.button("Start Analysing"):
                    switch_view('analysis')  # Call function to create "analysis" view and update view
            else:
                st.error("Failed to load CSV file.")
        else:
            st.info("Please upload a CSV file.")

elif st.session_state.view == 'analysis':  # Here we display the "Upload" view if the session state == "analysis"
    st.header("Choose what you want to analyse!:chart_with_upwards_trend:")
    st.write("Please choose from the following options. After that, click the 'Start Analyzing' button to display "
             "your selected view and begin the analysis.")

    # Create three parallel sections
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.subheader("Customer Analytics")
        st.write("- Identify the most and least profitable customers. \n"
                 "- Gain knowledge about our customer's payment methods. \n"
                 "- Interactively filter the data.")

    with col2:
        st.subheader("Market Analytics")
        st.write("- Compare the total sales by market. \n"
                 "- Compare the mean sales by market. \n"
                 "- Interactively filter the data."
                 )

    with col3:
        st.subheader("Sales Analytics")
        st.write("- Compare total sales by product categories. \n"
                 "- Gain insights about sales performance and visualize trends. \n"
                 "- Interactively filter the data.")

    with col4:
        st.subheader("Profit Analytics")
        st.write("- Gain insights about the company profitability. \n"
                 "- Visualize profit performance of different segments. \n"
                 "- Interactively filter the data.")

    with col5:
        st.subheader("Product Analytics")
        st.write("- Identify top/least selling products \n"
                 "- Analyse profit by product category \n"
                 "- Sales trends over time"
                 )

    # Columns to display the buttons that switch to the respective analytics view
    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
        if st.button("Start analysing", key="button5"):
            switch_view('customer')
    with col7:
        if st.button("Start analysing", key="button6"):
            switch_view('market')
    with col8:
        if st.button("Start analysing", key="button7"):
            switch_view('sales')
    with col9:
        if st.button("Start analysing", key="button8"):
            switch_view('profit')
    with col10:
        if st.button("Start analysing", key="button9"):
            switch_view('product')

    if st.button("Go back to Upload",
                 type="secondary"):  # If this button is pressed, the user returns to the defined view.
        switch_view('upload')  # switch_view function called with parameter "upload"

elif st.session_state.view == 'customer':  # Here we display the "Upload" view if the session state == "customer"

    customer_scenario.customer_logic()  # Call customer logic method from CustomerScenario class

elif st.session_state.view == 'market':

    market_scenario.market_logic()

elif st.session_state.view == 'sales':

    sales_scenario.SalesScenario().sales_logic()

elif st.session_state.view == 'profit':
    profitability_scenario.profit_logic()

elif st.session_state.view == 'product':
    product_scenario.ProductScenario().product_logic()