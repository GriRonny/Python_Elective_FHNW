import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


def customer_logic():
    st.header("Customer Section")

    # Error Handling here? Because data might be empty?

    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # assigning session state df to variable "df"

        # Sidebar with checkboxes for markets
        with st.sidebar:
            st.header("Filter by Market")
            markets = df['Market'].unique()
            selected_markets = [st.checkbox(market, key=market) for market in markets]

        # Sidebar for Segment Filter
        with st.sidebar:
            st.header("Filter by Segment")
            seg_type = df['Segment'].unique()
            selected_seg = [st.checkbox(segment, key=segment) for segment in seg_type]

        # Create lists of selected markets and segments
        selected_market_list = [market for market, selected in zip(markets, selected_markets) if selected]
        selected_segment_list = [segment for segment, selected in zip(seg_type, selected_seg) if selected]

        # Filter the DataFrame based on selected markets and segments
        if selected_market_list and selected_segment_list:
            filtered_df = df[
                (df['Market'].isin(selected_market_list)) &
                (df['Segment'].isin(selected_segment_list))
                ]
        elif selected_market_list:
            filtered_df = df[df['Market'].isin(selected_market_list)]
        elif selected_segment_list:
            filtered_df = df[df['Segment'].isin(selected_segment_list)]
        else:
            filtered_df = df  # If no filters selected, use original/unfiltered df

        sales_chart = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('Market:O', sort='-y', title='Market'),
            y=alt.Y('sum(Sales):Q', title='Total Sales'),
            color='Market:N',
            tooltip=['Market', 'sum(Sales)']  # Displayed when hovering over a bar
        ).properties(
            width=600,
            height=400,
            title='Total Sales by Market'
        )

        st.altair_chart(sales_chart, use_container_width=True)

        payment_counts = filtered_df['Payment Method'].value_counts().reset_index()
        payment_counts.columns = ['Payment Method', 'Count']

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
