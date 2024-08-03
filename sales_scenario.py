import streamlit as st
import pandas as pd
import altair as alt

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
            # Extract unique countries from "Country" column and convert to list
            country_list = df["Country"].unique().tolist()

            # Sidebar for Sales Scenario
            with st.sidebar:
                st.header("Filter options:")

                selected_countries = st.multiselect(
                    "Select Countries",
                    options=country_list,
                    default=country_list[0:3]
                )

                selected_years = st.multiselect(
                    "Select Years",
                    options=order_years_list,
                    default=order_years_list[0:2]
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
                    st.subheader("Sales Overview")
                    st.bar_chart(data=filtered_df["Sales"])

                    # This groups the df by country and appends aggregates of one or more columns
                    sales_summary = df.groupby('Country').agg({'Sales': 'sum', 'Profit': 'mean'}).reset_index()

                    sorted_sales_summary = sales_summary.sort_values(by="Sales", ascending=False)

                    top_3_countries = sorted_sales_summary.head(3)
                    flop_3_countries = sorted_sales_summary.tail(3)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("Countries with the highest Sales:")
                        st.dataframe(top_3_countries)

                    with col2:
                        st.write("Countries with the lowest Sales:")
                        st.dataframe(flop_3_countries)

                    # Country specific analysis for selected countries
                    for country in selected_countries:
                        country_df = filtered_df[filtered_df['Country'] == country]

                        if country_df.empty:
                            st.info(f"No data available for {country} with current filter applied.", icon='⚠️')
                        else:
                            st.header(f"Country specific analysis for {country}")

                            col1, col2 = st.columns(2)

                            with col1:
                                chart_title = f"Sales by Category for {country}"
                                # --- BARCHART_SALES_PER_CATEGORY ---
                                sales_category = alt.Chart(country_df).mark_bar().encode(
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

                            with col2:
                                # --- BARCHART_SALES_PER_SUB_CATEGORY ---
                                chart_title_2 = f"Sales by Sub-Category for {country}"
                                sales_sub_category = alt.Chart(country_df).mark_bar().encode(
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

                            product_name_count = country_df['Product Name'].value_counts().reset_index()
                            top_5_products = product_name_count.head(5)
                            st.subheader(f"The 5 most sold products in {country} are:")
                            st.write(top_5_products)

            else:
                st.warning("No sales data available with current filter applied.", icon="⚠️")

        else:
            st.warning("No data available. Please upload a dataset.")

        if st.button("Go back to Analysis"):
            st.session_state.switch_view('analysis')
