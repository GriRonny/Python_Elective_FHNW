import streamlit as st
import pandas as pd
import numpy as np


class SalesScenario:
    def __init__(self):
        pass

    def sales_logic(self):
        st.header("Sales Section")

        if st.session_state.df is not None:  # Checking if session state df is not empty
            df = st.session_state.df  # assigning session state df to variable "df"

            st.bar_chart(data=df["Sales"])

            # This groups the df by country and appends aggregates of one or more columns
            sales_summary = df.groupby('Country').agg({'Sales': 'sum', 'Profit': 'mean'}).reset_index()
            #sales_summary = df.groupby('Country')['Sales'].sum().reset_index()  # needed because return must be columns

            # Rename columns (not working just now)
            #sales_summary.rename(columns={'Sales': 'Total Sales', 'Profit': 'Mean Profit'}, inplace=True)

            sorted_sales_summary = sales_summary.sort_values(by="Sales", ascending=False)

            top_3_countries = sorted_sales_summary.head(3)
            flop_3_countries = sorted_sales_summary.tail(3)

            st.write("Countries with the highest Sales:")
            st.dataframe(top_3_countries)

            st.write("Countries with the lowest Sales:")
            st.dataframe(flop_3_countries)

        if st.button("Go back to Analysis"):
            st.session_state.switch_view('analysis')
