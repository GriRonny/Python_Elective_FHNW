import streamlit as st
import pandas as pd
import altair as alt


class SalesScenario:
    def __init__(self):
        pass

    def sales_logic(self):
        st.header("Sales Section")

        st.write("""
        Welcome to the Sales Analysis Section. Use the filters on the left sidebar to select the desired product 
        categories and years. You may also adjust the order date range to narrow down the data further. 
        The visualizations and data tables will update accordingly to reflect your selections.
        """)

        if st.session_state.df is not None:  # Checking if session state df is not empty
            df = st.session_state.df  # Assigning session state df to variable "df"

            # Convert "Order Date" column to datetime
            df["Order Date"] = pd.to_datetime(df["Order Date"])

            # Extract unique years from "Order Date" column and convert to list
            order_years_list = df["Order Date"].dt.year.unique().tolist()
            # Extract unique product categories from "Category" column and convert to list
            category_list = df["Category"].unique().tolist()

            # Sidebar for Sales Scenario
            with st.sidebar:
                st.header("Filter Options")

                selected_categories = st.multiselect(
                    "Product Categories:",
                    options=category_list,
                    default=category_list
                )

                selected_years = st.multiselect(
                    "Select Year(s):",
                    options=order_years_list,
                    default=order_years_list[-1]
                )

                if selected_years:
                    df_filtered_by_year = df[df["Order Date"].dt.year.isin(selected_years)]
                    # Extract unique dates from "Order Date" column and convert to list
                    order_dates_list = df_filtered_by_year["Order Date"].dt.date.unique().tolist()

                    date_range = st.slider(
                        "Order Date Range:",
                        min_value=min(order_dates_list),
                        max_value=max(order_dates_list),
                        value=(min(order_dates_list), max(order_dates_list)),
                        format="YYYY-MM-DD"
                    )

                # Returns user to overview view
                if st.button("Return to overview"):
                    st.session_state.switch_view('analysis')

            if selected_years:
                df_filtered_by_year = df[df["Order Date"].dt.year.isin(selected_years)]

                filtered_df = df_filtered_by_year.query(
                    "`Order Date` >= @pd.Timestamp(@date_range[0]) and `Order Date` <= @pd.Timestamp(@date_range[1]) "
                    "and `Category` in @selected_categories"
                )

                # Display warning if df empty
                if filtered_df.empty:
                    st.warning("No sales data available with current filter applied.", icon='⚠️')
                else:
                    # Display the sales bar chart
                    st.subheader("Sales Overview")

                    # Enhanced Bar Chart
                    sales_chart = alt.Chart(filtered_df).mark_bar().encode(
                        x=alt.X('Category:O', sort='-y', title='Category'),
                        y=alt.Y('sum(Sales):Q', title='Total Sales'),
                        color=alt.Color('Category:N', legend=None, scale=alt.Scale(scheme='category20b')),
                        tooltip=['Category', 'sum(Sales)']
                    ).properties(
                        width=700,
                        height=400,
                        title='Total Sales by Category'
                    ).configure_axis(
                        labelFontSize=12,
                        titleFontSize=14
                    ).configure_title(
                        fontSize=16
                    ).configure_view(
                        strokeOpacity=0
                    ).interactive()

                    st.altair_chart(sales_chart, use_container_width=True)

                    # This groups the df by sub-category and appends aggregates of one or more columns
                    sales_summary = df.groupby('Sub-Category').agg({'Sales': 'sum'}).reset_index()

                    sorted_sales_summary = sales_summary.sort_values(by="Sales", ascending=False)

                    top_5_sub_categories = sorted_sales_summary.head(5)
                    flop_5_sub_categories = sorted_sales_summary.tail(5)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Sub-Categories with the Highest Sales:**")
                        st.dataframe(top_5_sub_categories)

                    with col2:
                        st.write("**Sub-Categories with the Lowest Sales:**")
                        st.dataframe(flop_5_sub_categories)

                    # Category specific analysis for selected categories
                    for category in selected_categories:
                        category_df = filtered_df[filtered_df['Category'] == category]

                        if category_df.empty:
                            st.info(f"No data available for {category} with current filter applied.", icon='⚠️')
                        else:
                            st.subheader(f"Category Specific Analysis for _{category}_", divider="gray")

                            chart_title = f"Sales by Sub-Category for Category {category}"

                            sales_sub_category = alt.Chart(category_df).mark_bar().encode(
                                x=alt.X('Sub-Category:O', sort='-y', title='Sub-Category'),
                                y=alt.Y('sum(Sales):Q', title='Sales per Sub-Category'),
                                color='Sub-Category:N',
                                tooltip=['Sub-Category', 'sum(Sales)']  # Displayed when hovering over a bar
                            ).properties(
                                width=600,
                                height=400,
                                title=chart_title
                            )

                            st.altair_chart(sales_sub_category, use_container_width=True)

                            product_sales_summary = category_df.groupby('Product Name').agg({'Sales': 'sum'}).reset_index()

                            sorted_prod_sum = product_sales_summary.sort_values(by="Sales", ascending=False)

                            top_5_products = sorted_prod_sum.head(5)
                            st.write(f"**Top Five Most Sold Products in {category}**")
                            st.dataframe(top_5_products)

                            # Line chart for sales trend over time
                            sales_trend_chart = alt.Chart(category_df).mark_line().encode(
                                x=alt.X('yearmonth(Order Date):T', title='Order Date (Year-Month)'),
                                y='sum(Sales):Q',
                                color='Sub-Category:N',
                                tooltip=['Order Date:T', 'sum(Sales)', 'Sub-Category']
                            ).properties(
                                width=600,
                                height=400,
                                title=f'Sales Trend Over Time for {category}'
                            )

                            st.altair_chart(sales_trend_chart, use_container_width=True)

            else:
                st.warning("No sales data available with current filter applied.", icon="⚠️")

        else:
            st.warning("No data available. Please upload a dataset.")
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            if uploaded_file is not None:
                try:
                    st.session_state.df = pd.read_csv(uploaded_file)
                    st.success("File uploaded successfully!")
                except Exception as e:
                    st.error(f"Error uploading file: {e}")

        if st.button("Go back to Analysis"):
            st.session_state.switch_view('analysis')


# Initialize and run the app
if __name__ == "__main__":
    scenario = SalesScenario()
    scenario.sales_logic()
