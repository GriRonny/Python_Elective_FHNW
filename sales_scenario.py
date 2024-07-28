import streamlit as st
import pandas as pd
import numpy as np


class SalesScenario:
    def __init__(self):
        pass

    def sales_logic(self):
        st.header("👷WIP👷: Sales Section")

        if st.session_state.df is not None:  # Checking if session state df is not empty
            df = st.session_state.df  # Assigning session state df to variable "df"

            # Convert "Order Date" column to datetime
            df["Order Date"] = pd.to_datetime(df["Order Date"])

            # Extract unique years from "Order Date" column and convert to list
            order_years_list = df["Order Date"].dt.year.unique().tolist()
            # Extract unique countries from "Countries" column and convert to list
            country_list = df["Country"].unique().tolist()

            # Sidebar for Sales Scenario
            with st.sidebar:
                st.header("Filter options:")

                selected_countries = st.multiselect(
                    "Select Countries",
                    options=country_list,
                    default=country_list[0]
                )

                selected_years = st.multiselect(
                    "Select Years",
                    options=order_years_list,
                    default=order_years_list
                )

                if selected_years:
                    df_filtered_by_year = df[df["Order Date"].dt.year.isin(selected_years)]
                    # Extract unique dates from "Order Date" column and convert to list
                    order_dates_list = df_filtered_by_year["Order Date"].dt.date.unique().tolist()

                    date_range = st.slider(
                        "Order Date",
                        min_value=min(order_dates_list),
                        max_value=max(order_dates_list),
                        value=(min(order_dates_list), max(order_dates_list))
                    )

                    # Returns user to overview view
                    if st.button("Return to overview"):
                        st.session_state.switch_view('analysis')

            if selected_years:
                filtered_df = df_filtered_by_year.query(
                    "`Order Date` >= @pd.Timestamp(@date_range[0]) and `Order Date` <= @pd.Timestamp(@date_range[1]) "
                    "and `Country` in @selected_countries"
                )

                # Display warning if df empty
                if filtered_df.empty:
                    st.warning("No sales data available with current filter applied.", icon='⚠️')
                else:
                    # Display the sales bar chart
                    st.bar_chart(data=filtered_df["Sales"])

                    # This groups the df by country and appends aggregates of one or more columns
                    sales_summary = df.groupby('Country').agg({'Sales': 'sum', 'Profit': 'mean'}).reset_index()

                    sorted_sales_summary = sales_summary.sort_values(by="Sales", ascending=False)

                    top_3_countries = sorted_sales_summary.head(3)
                    flop_3_countries = sorted_sales_summary.tail(3)

                    st.write("Countries with the highest Sales:")
                    st.dataframe(top_3_countries)

                    st.write("Countries with the lowest Sales:")
                    st.dataframe(flop_3_countries)
            else:
                st.warning("No sales data available with current filter applied.", icon="⚠️")

        else:
            st.warning("No data available. Please upload a dataset.")

        if st.button("Go back to Analysis"):
            st.session_state.switch_view('analysis')
