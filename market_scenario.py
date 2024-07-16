import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


def market_logic():
    st.header("Market Analytics")

    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # assigning session state df to variable "df"

        # Sidebar with checkboxes for markets
        st.sidebar.header("Please Filter Here:")
        # "market" is a list of Strings
        market = st.sidebar.multiselect(
            "Select Markets:",
            options=df['Market'].unique(),
            default=df['Market'].unique()
        )

        # NEW LOGIC TO FILTER THE DATA USING QUERY() FUNCTION!
        # Select all datapoints where column "Market" of DF has matches with contents of local variable "market"
        df_filtered_market = df.query("Market == @market")

        countries = st.sidebar.multiselect(
            "Select Countries:",
            options=df_filtered_market['Country'].unique()
        )

        df_filtered_countries = df_filtered_market.query("Country == @countries")

        # --- CODE FOR THE CHARTS ---
        # Creating two columns for the
        col1, col2 = st.columns(2)
        with col1:
            # --- BARCHART_SALES ---
            sales_chart = alt.Chart(df_filtered_market).mark_bar().encode(
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

        with col2:
            avg_sales_chart = alt.Chart(df_filtered_market).mark_bar().encode(
                x=alt.X('Market:O', sort='-y', title='Market'),
                y=alt.Y('mean(Sales):Q', title='Average Sales'),
                color='Market:N',
                tooltip=['Market', 'mean(Sales)']  # Displayed when hovering over a bar
            ).properties(
                width=600,
                height=400,
                title='Average Total Sales by Market'
            )

            st.altair_chart(avg_sales_chart, use_container_width=True)

        if df_filtered_countries.empty:
            st.header("First select a country to further analyse the sales by product category.")

        else:
            chart_title = f"Total Sales by Category for Country: {countries}"
            # --- BARCHART_SALES_PER_CATEGORY ---
            sales_category = alt.Chart(df_filtered_countries).mark_bar().encode(
                x=alt.X('Category:O', sort='-y', title='Category'),
                y=alt.Y('sum(Sales):Q', title='Total Sales per Category'),
                color='Category:N',
                tooltip=['Category', 'sum(Sales)']  # Displayed when hovering over a bar
            ).properties(
                width=600,
                height=400,
                title=chart_title
            )

            st.altair_chart(sales_category, use_container_width=True)

    else:
        st.error("No data loaded. Please upload a CSV file.")

    with st.sidebar:
        if st.button("Return to overview"):
            st.session_state.switch_view('analysis')


class MarketScenario:
    def __init__(self):
        pass
