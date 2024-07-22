import streamlit as st
import pandas as pd
import customer_scenario
import sales_scenario
import market_scenario
import profitability_scenario

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

    st.header("Welcome to our dashboard :eggplant:")

    st.write("First, select the latest global_superstore.csv file. \n"
             "\nNext, enjoy our dashboard that we created!:fire:")

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
                st.error(f"Missing columns: {', '.join(missing_columns)}. Please check your CSV file.")
                return None  # Return an empty df
            else:
                return df_check  # Return valid df

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
            if st.button("Start Analysing"):
                switch_view('analysis')  # Call function to create "analysis" view and update view
        else:
            st.error("Failed to load CSV file.")
    else:
        st.info("Please upload a CSV file.")

elif st.session_state.view == 'analysis':  # Here we display the "Upload" view if the session state == "analysis"
    st.header("Choose what you want to analyse!:chart_with_upwards_trend:")
    st.write("Below are the different analyses.")

    # Create three parallel sections
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader("Customer Analytics")
        st.write("- Identify most/least profitable customers \n"
                 "- Gain insights about payment methods \n"
                 "- Interactively filter the data")

    with col2:
        st.subheader("Market Analytics")
        st.write("- Compare total sales per market \n"
                 "- Compare mean sales per market \n"
                 "- Filter the data by desired market"
                 )

    with col3:
        st.subheader("Sales Analytics")
        st.write("- Identify most/least profitable customers \n"
                 "- Gain insights about payment methods \n"
                 "- Interactively filter the data")

    with col4:
        st.subheader("Profitability Analytics")
        st.write("- Identify most/least profitable customers \n"
                 "- Gain insights about payment methods \n"
                 "- Interactively filter the data")

    # Columns to display the buttons that switch to the respective analytics view
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        if st.button("Start analysing", key="button5"):
            switch_view('customer')
    with col6:
        if st.button("Start analysing", key="button6"):
            switch_view('market')
    with col7:
        if st.button("Start analysing", key="button7"):
            switch_view('sales')
    with col8:
        if st.button("Start analysing", key="button8"):
            switch_view('profit')

    if st.button("Go back to Upload"):  # If this button is pressed, the user returns to the defined view.
        switch_view('upload')  # switch_view function called with parameter "upload"

elif st.session_state.view == 'customer':  # Here we display the "Upload" view if the session state == "customer"

    customer_scenario.customer_logic()  # Call customer logic method from CustomerScenario class

elif st.session_state.view == 'market':

    market_scenario.market_logic()

elif st.session_state.view == 'sales':

    sales_scenario.SalesScenario().sales_logic()

elif st.session_state.view == 'profit':
    profitability_scenario.profit_logic()
