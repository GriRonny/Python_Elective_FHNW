import streamlit as st
import pandas as pd
import altair as alt

def market_logic():
    st.header("Market Analytics")

    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # Assigning session state df to variable "df"

        # Sidebar with checkboxes for markets
        st.sidebar.header("Please Filter Here:")

        # Create list of unique markets
        market_list = df['Market'].unique().tolist()

        market = st.sidebar.multiselect(
            "Select Markets:",
            options=market_list,
            default=market_list
        )

        # Ensure the "Order Date" column is in datetime format
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Order Year'] = df['Order Date'].dt.year

        # Create list of unique years
        years_list = df['Order Year'].unique().tolist()

        year_select = st.sidebar.multiselect(
            'Select Years:',
            options=years_list,
            default=years_list[-1]
        )

        # Filter data using the selected markets and years
        df_filtered_market = df.query("Market in @market and `Order Year` in @year_select")

        # Filter the countries based on the selected markets
        country_list = df_filtered_market["Country"].unique().tolist()

        countries = st.sidebar.multiselect(
            "Select Countries:",
            options=country_list,
            #default=country_list[0] if country_list else []
        )

        df_filtered_countries = df_filtered_market.query("Country in @countries")
        country_str = ', '.join(countries)

        col1, col2 = st.columns(2)

        if df_filtered_market.empty:
            st.warning("No market data available with current filter applied.", icon='⚠️')
        else:
            with col1:
                sales_chart = alt.Chart(df_filtered_market).mark_bar().encode(
                    x=alt.X('Market:O', sort='-y', title='Market'),
                    y=alt.Y('sum(Sales):Q', title='Total Sales'),
                    color='Market:N',
                    tooltip=['Market', 'sum(Sales)']
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
                    tooltip=['Market', 'mean(Sales)']
                ).properties(
                    width=600,
                    height=400,
                    title='Average Total Sales by Market'
                )

                st.altair_chart(avg_sales_chart, use_container_width=True)

        if df_filtered_countries.empty:
            st.info("Select a country to analyze the sales by product category for the selected country", icon='💡')
        else:
            for country in countries:
                country_df = df_filtered_countries[df_filtered_countries['Country'] == country]

                if country_df.empty:
                    st.info(f"No data available for {country} with current filter applied.", icon='⚠️')
                else:
                    st.header(f"Country specific analysis for {country}")

                    col3, col4 = st.columns(2)

                    with col3:
                        chart_title = f"Sales by Category for {country}"
                        sales_category = alt.Chart(country_df).mark_bar().encode(
                            x=alt.X('Category:O', sort='-y', title='Category'),
                            y=alt.Y('sum(Sales):Q', title='Sales per Category'),
                            color='Category:N',
                            tooltip=['Category', 'sum(Sales)']
                        ).properties(
                            width=600,
                            height=400,
                            title=chart_title
                        )

                        st.altair_chart(sales_category, use_container_width=True)

                    with col4:
                        chart_title_2 = f"Sales by Sub-Category for {country}"
                        sales_sub_category = alt.Chart(country_df).mark_bar().encode(
                            x=alt.X('Sub-Category:O', sort='-y', title='Sub-Category'),
                            y=alt.Y('sum(Sales):Q', title='Sales per Sub-Category'),
                            color='Sub-Category:N',
                            tooltip=['Sub-Category', 'sum(Sales)']
                        ).properties(
                            width=600,
                            height=400,
                            title=chart_title_2
                        )

                        st.altair_chart(sales_sub_category, use_container_width=True)

                    product_name_count = country_df['Product Name'].value_counts().reset_index()
                    top_5_products = product_name_count.head(5)
                    st.subheader(f"The 5 most sold products in {country} are:")
                    st.write(top_5_products)

    else:
        st.error("No data loaded. Please upload a CSV file.")

    with st.sidebar:
        if st.button("Return to overview"):
            st.session_state.switch_view('analysis')


class MarketScenario:
    def __init__(self):
        pass
