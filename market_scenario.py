import streamlit as st
import pandas as pd
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

        # Code for the Year filter
        # Ensure the sales date column is in datetime format
        df['Order Date'] = pd.to_datetime(df['Order Date'])

        # Extract the year from the sales date
        df['Order Year'] = df['Order Date'].dt.year

        # Get unique sales years
        unique_years = df['Order Year'].unique()
        # create sidebar selection with the years
        year_select = st.sidebar.multiselect('Select Year:', options=unique_years, default=unique_years)

        # NEW LOGIC TO FILTER THE DATA USING QUERY() FUNCTION!
        # Select all data points where column "Market" of DF has matches with contents of local variable "market"
        df_filtered_market = df.query("Market == @market & @df['Order Year'] == @year_select")

        countries = st.sidebar.multiselect(
            "Select a country:",
            options=df_filtered_market['Country'].unique(),
            max_selections=1
        )

        df_filtered_countries = df_filtered_market.query("Country == @countries")
        # Convert list of countries to a string, this helps to get rid of the [''] when displaying the country name
        country_str = ', '.join(countries)

        # --- CODE FOR THE CHARTS ---
        # Creating two columns for the
        col1, col2 = st.columns(2)

        if df_filtered_market.empty:
            st.warning("No market data available with current filter applied.", icon='⚠️')

        else:
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

        # If no countries are selected, an info will be displayed
        if df_filtered_countries.empty:
            st.info(":bulb: Select a country to analyze the sales by product category for the selected country")

        else:
            st.header(f"Country specific analysis for {country_str}")
            # Columns for the two subsequent charts
            col3, col4 = st.columns(2)

            with col3:
                chart_title = f"Sales by Category for {country_str}"
                # --- BARCHART_SALES_PER_CATEGORY ---
                sales_category = alt.Chart(df_filtered_countries).mark_bar().encode(
                    x=alt.X('Category:O', sort='-y', title='Category'),
                    y=alt.Y('sum(Sales):Q', title='Sales per Category'),
                    color='Category:N',
                    tooltip=['Category', 'sum(Sales)']  # Displayed when hovering over a bar
                ).properties(
                    width=600,
                    height=400,
                    title=chart_title
                )

                st.altair_chart(sales_category, use_container_width=True)

            with col4:
                # --- BARCHART_SALES_PER_SUB_CATEGORY ---
                chart_title_2 = f"Sales by Sub-Category for {country_str}"
                sales_sub_category = alt.Chart(df_filtered_countries).mark_bar().encode(
                    x=alt.X('Sub-Category:O', sort='-y', title='Sub-Category'),
                    y=alt.Y('sum(Sales):Q', title='Sales per Sub-Category'),
                    color='Sub-Category:N',
                    tooltip=['Sub-Category', 'sum(Sales)']  # Displayed when hovering over a bar
                ).properties(
                    width=600,
                    height=400,
                    title=chart_title_2
                )

                st.altair_chart(sales_sub_category, use_container_width=True)

            product_name_count = df_filtered_countries['Product Name'].value_counts().reset_index()
            top_5_products = product_name_count.head(5)
            st.subheader(f"The 5 most sold products in {country_str} are:")
            st.write(top_5_products)

    else:
        st.error("No data loaded. Please upload a CSV file.")

    with st.sidebar:
        if st.button("Return to overview"):
            st.session_state.switch_view('analysis')


class MarketScenario:
    def __init__(self):
        pass
