import streamlit as st
import pandas as pd
import numpy as np


class CustomerScenario:
    def __init__(self):  # Empty constructor
        pass

    def customer_logic(self):
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
            filtered_df = df[
                df['Market'].isin([market for market, selected in zip(markets, selected_markets) if selected])]

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
            st.session_state.switch_view('analysis')


