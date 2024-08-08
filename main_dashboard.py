import streamlit as st
import pandas as pd
import customer_scenario
import sales_scenario
import market_scenario
import profitability_scenario
import product_scenario
import json
import time
import base64
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Business Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")


# Load Lottie animation
def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)


# Polarbear Lotti animation
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
    # Centralization of "Welcome" text
    empty_col1, centered_col, empty_col2 = st.columns([1, 2, 1])
    with centered_col:
        st.markdown("## Welcome to Your Business Dashboard 📊")

    # Centralization of "submessage"
    empty_col1, centered_col, empty_col2 = st.columns([1, 2, 1])
    with centered_col:
        st.markdown("### Get Started with Your Business Insights!")

        st.write("")

    # Alignment of Polar Bear Lotti Animation
    empty_col1, col1, welcome_col, col2, empty_col2 = st.columns([1, 2, 0.01, 2, 1])
    with col1:
        st_lottie(lottie_polar_bear, height=400, key="polar_bear")

    with col2:
        st.markdown("#### Start by uploading your data file")
        st.write("To upload your data file, please follow these steps:")
        st.write("1. Select the latest global_superstore.csv file.")
        st.write("2. Drag and drop the file into the area below or click 'Browse files' to select it.")
        st.write("3. Click 'Start Analysing' to analyse your data.")

        # Define required columns as a constant variable
        REQUIRED_COLUMNS = [
            "Order Date", "Ship Date", "Ship Mode", "Customer Name", "Customer DOB", "Segment", "City", "State",
            "Country",
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
            with st.spinner("Processing file..."):  # Spinner to symbolize processing of file
                time.sleep(1)  # Add a delay for processing
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
            st.info("Please upload your CSV file.")

elif st.session_state.view == 'analysis':  # Here we display the "Upload" view if the session state == "analysis"


    # CSS styling for the cards and buttons
    st.markdown("""
        <style>
        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }
        .card {
            background-color: #c4b5fd;
            border: 1px solid #c4b5fd;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin: 10px;
            padding: 20px;
            text-align: left;  /* Center align the text and image */
            width: 300px;
            display: inline-block;
            vertical-align: top;
        }
        .card img {
            width: 200;
            height: auto;
            display: block;  /* Center the image */
            margin-left: auto;  /* Center the image */
            margin-right: auto;  /* Center the image */
        }
        .card h3 {
         margin-bottom:30px:
            font-size: 30px;
        }
        .card p {
            font-size: 25px;
            line-height: 2;
            color: white;
        }


                }
        </style>
        """, unsafe_allow_html=True)


    # Function to create a card
    def create_card(image_path, title, description, bg_color, text_color):
        # Read the image file and convert it to a base64 string
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode()

        st.markdown(f"""
            <div class="card" style="background-color: {bg_color}; border: 1px solid {bg_color}; padding: 10px; border-radius: 5px;">
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{image_data}" alt="{title}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 20%;">
                </div>
                <h3 style="color: {text_color};">{title}</h3>
                <p>{description}</p>
                           </div>
        """, unsafe_allow_html=True)


    # Layout the cards
    col1, empty_col1, empty_col2, col2 = st.columns([7,1,1,1])
    with col1:
        st.markdown("# Your Analytics Dashboard")
        st.markdown("### For detailed reports, please click 'Start Analyzing' under the desired category.")

        st.markdown('<div class="container">', unsafe_allow_html=True)

    with col2:
        st.image("assets/bar.png", width=200)

    # Create parallel sections
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        create_card("assets/picture1.png", "Customer Analytics",
                    "• Identify profitable customers.<br>• Understand payment methods.<br>• Interactive data filtering.",
                    "#c4b5fd", "#6c63ff")

    with col2:
        create_card("assets/picture2.png", "Market Analytics",
                    "• Compare total sales by market.<br>• Compare mean sales by market.<br>• Interactive data filtering.",
                    "#92d173", "#4b8b3b")

    with col3:
        create_card("assets/picture3.png", "Sales Analytics",
                    "• Compare sales by products.<br>• Visualize sales performance trends.<br>• Interactive data filtering.",
                    "#b5dcff", "#6394ff")

    with col4:
        create_card("assets/picture4.png", "Profit  Analytics",
                    "• Insights into profitability Analytics.<br>• Visualize segment performance.<br>• Interactive data filtering.",
                    "#fdc4c4", "#ff6363")

    with col5:
        create_card("assets/picture5.png", "Product Analytics",
                    "• Identify top/least selling products.<br>• Analyze profit by category.<br>• Sales trends over time.",
                    "#ffe8b5", "#ffc163")

    st.markdown('</div>', unsafe_allow_html=True)

    # Columns to display the buttons that switch to the respective analytics view
    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
        if st.button("Start Analysing", key="button5"):
            switch_view('customer')

    with col7:
        if st.button("Start Analysing", key="button6"):
            switch_view('market')
    with col8:
        if st.button("Start Analysing", key="button7"):
            switch_view('sales')
    with col9:
        if st.button("Start Analysing", key="button8"):
            switch_view('profit')
    with col10:
        if st.button("Start Analysing", key="button9"):
            switch_view('product')

    st.write("")
    st.write("")
    st.markdown(
                "### To restart the process with a new dataset, please click the button below to return to the upload page.")

    if st.button("Go back to Upload",
    type="secondary"):  # If this button is pressed, the user returns to the defined view.
                switch_view('upload')  # switch_view function called with parameter "upload"
                st.experimental_rerun()

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

