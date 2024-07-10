import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="centered", initial_sidebar_state="expanded")


def load_csv(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        st.error("Something went wrong")
        return None


# Initialize session state
if 'view' not in st.session_state:
    st.session_state.view = 'upload'  # Create default view


# Function to switch view
def switch_view(view_name):
    st.session_state.view = view_name  # Create view according to passed parameter
    st.rerun()  # Trigger rerun everytime function is called to update view accordingly.


if st.session_state.view == 'upload':  # Display the "Upload" view if the session state == "upload"

    st.header("Upload CSV file")

    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
             "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
             "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in."
             "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer in.")

    uploaded_csv = st.file_uploader("Choose a CSV file to be processed.", type="csv")

    if uploaded_csv is not None:
        df = load_csv(uploaded_csv)
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
            switch_view('product')

    if st.button("Go back to Upload"):  # If this button is pressed, the user returns to the defined view.
        switch_view('upload')  # switch_view function called with parameter "upload"

elif st.session_state.view == 'customer':  # Here we display the "Upload" view if the session state == "customer"

    st.header("Customer Section")
    # Error Handling here? Because data might be empty?

    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # assigning session state df to variable "df"

        # Sidebar with checkboxes for markets
        with st.sidebar:
            st.header("Filter by Market")
            markets = df['Market'].unique()
            selected_markets = [st.checkbox(market, key=market) for market in markets]

        # Filter the DataFrame based on selected markets
        filtered_df = df[df['Market'].isin([market for market, selected in zip(markets, selected_markets) if selected])]

        # If no markets are selected, use the original DataFrame
        if filtered_df.empty:
            filtered_df = df

        st.bar_chart(filtered_df["Sales"])

        payment_counts = filtered_df['Payment Method'].value_counts().reset_index()
        payment_counts.columns = ['Payment Method', 'Count']

        # Display the bar chart
        st.bar_chart(payment_counts.set_index('Payment Method'))
    else:
        st.error("No data loaded. Please upload a CSV file.")

    # Sidebar with radio buttons
    with st.sidebar:
        add_radio = st.radio(
            "This is a radio button selection.",
            ("Option 1", "Option 2", "Option 3")
        )

    if st.button("Go back to Analysis"):
        switch_view('analysis')

elif st.session_state.view == 'market':
    st.header("Market Section")

    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # assigning session state df to variable "df"

        st.bar_chart(data=df["Sales"])

    if st.button("Go back to Analysis"):
        switch_view('analysis')

elif st.session_state.view == 'product':
    st.header("Product Section")

    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # assigning session state df to variable "df"

        st.bar_chart(data=df["Sales"])

    if st.button("Go back to Analysis"):
        switch_view('analysis')
