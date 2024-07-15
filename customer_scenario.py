import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


def customer_logic():
    st.header("Customer Analyses")

    # Error Handling here? Because data might be empty?

    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # assigning session state df to variable "df"

        # Sidebar for Segment Filter
        with st.sidebar:
            st.header("Please Filter Here")
            st.subheader("Filter by Customer Segment")
            seg_type = df['Segment'].unique()
            selected_seg = [st.checkbox(segment, key=segment) for segment in seg_type]

        # Create lists of selected segments
        selected_segment_list = [segment for segment, selected in zip(seg_type, selected_seg) if selected]

        # sidebar menu to select years
        with st.sidebar.subheader('Select relevant year'):
            # Ensure the sales date column is in datetime format
            df['Order Date'] = pd.to_datetime(df['Order Date'])

            # Extract the year from the sales date
            df['Order Year'] = df['Order Date'].dt.year

            # Get unique sales years
            unique_years = df['Order Year'].unique()

            # create sidebar selection with the years
            year_select = st.sidebar.multiselect('Select Year', options=unique_years)

        # Filter the DataFrame based on selected segment and year
        if selected_segment_list and year_select:
            filtered_df = df[
                (df['Segment'].isin(selected_segment_list) & df['Order Year'].isin(year_select))
            ]
        elif selected_segment_list:
            filtered_df = df[df['Segment'].isin(selected_segment_list)]
        elif year_select:
            filtered_df = df[df['Order Year'].isin(year_select)]
        else:
            filtered_df = df  # If no filters selected, use original/unfiltered df

        payment_counts = filtered_df['Payment Method'].value_counts().reset_index()
        payment_counts.columns = ['Payment Method', 'Count']

        # Code to identify best customers
        most_profitable_cus = filtered_df.groupby('Customer Name')['Profit'].sum().reset_index()
        top_profitable_cus = most_profitable_cus.sort_values(by='Profit', ascending=False).head(3)

        # Code to identify the worst customers
        least_profitable_cus = filtered_df.groupby('Customer Name')['Profit'].sum().reset_index()
        top_worst_cus = least_profitable_cus.sort_values(by='Profit', ascending=True).head(3)

        # Displaying best and worst customers
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most profitable customers:+1:")
            st.write(top_profitable_cus)

        with col2:
            st.subheader("Least profitable customers:-1:")
            st.write(top_worst_cus)

        # Add a title above the bar chart
        st.subheader("Favored payment method of all customers :credit_card:")

        # Display the bar chart
        st.bar_chart(payment_counts.set_index('Payment Method'))

    else:
        st.error("No data loaded. Please upload a CSV file.")

    with st.sidebar:
        if st.button("Return to overview"):
            st.session_state.switch_view('analysis')


class CustomerScenario:
    def __init__(self):  # Empty constructor
        pass
