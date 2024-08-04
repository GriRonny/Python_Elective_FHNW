import streamlit as st
import pandas as pd
import altair as alt

def profit_logic():
    st.header("Profitability Section")

    st.markdown("""
    Welcome to the Profitability Analysis Section. Use the filters on the left sidebar to select the desired product categories and years.
    You can also adjust the order date range to narrow down the data further. The visualizations and data tables will update accordingly
    to reflect your selections, providing insights into profitability performance by market, country, category, sub-category, and customer.
    """)

    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # Assigning session state df to variable "df"

        # Convert "Order Date" column to datetime
        df["Order Date"] = pd.to_datetime(df["Order Date"])

        # Extract unique years from "Order Date" column and convert to list
        order_years_list = df["Order Date"].dt.year.unique().tolist()
        # Extract unique product categories from "Category" column and convert to list
        category_list = df["Category"].unique().tolist()

        # Sidebar for Profit Scenario
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
                st.warning("No profitability data available with current filter applied.", icon='⚠️')
            else:
                # Display the profitability overview
                st.subheader("Profitability Overview")

                # Calculate total profit and profit margin
                total_profit = filtered_df['Profit'].sum()
                total_sales = filtered_df['Sales'].sum()
                profit_margin = (total_profit / total_sales) * 100

                # Calculate expected profit for comparison
                expected_profit = 0.50 * total_sales  # We assume  15% of total sales as expected profit (tobe changed)
                profit_diff = total_profit - expected_profit

                if profit_diff < 0:
                    st.toast("Warning: Actual profit is less than expected profit for selected period.", icon="🚨")

                # Display profit statistics
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Total Profit", f"${total_profit:,.2f}")  # ,.2f = two decimals (thousands with comma)
                    st.metric("Profit Margin", f"{profit_margin:.2f}%")

                with col2:
                    st.metric("Expected Profit", f"${expected_profit:,.2f}")
                    st.metric("Profit Difference", f"${profit_diff:.2f}")

                # Monthly Profit Trend
                monthly_profit_trend = filtered_df.groupby(pd.Grouper(key='Order Date', freq='ME')).agg(
                    {'Profit': 'sum'}).reset_index()
                monthly_profit_trend_chart = alt.Chart(monthly_profit_trend).mark_line(point=True).encode(
                    x=alt.X('yearmonth(Order Date):T', title='Month'),
                    y=alt.Y('Profit:Q', title='Total Profit'),
                    tooltip=['yearmonth(Order Date)', 'Profit']
                ).properties(
                    width=800,
                    height=400,
                    title=alt.Title("Monthly Profit Trend", fontWeight="bolder")
                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14
                ).configure_title(
                    fontSize=16
                ).configure_view(
                    strokeOpacity=0
                )

                st.altair_chart(monthly_profit_trend_chart, use_container_width=True)

                # Group by market, country, category, sub-category, and customer to calculate total profit
                market_profit = (filtered_df.groupby('Market').agg({'Profit': 'sum'}).reset_index()
                                 .sort_values(by='Profit', ascending=False).head(5))
                country_profit = (filtered_df.groupby('Country').agg({'Profit': 'sum'}).reset_index()
                                  .sort_values(by='Profit', ascending=False).head(5))
                category_profit = (filtered_df.groupby('Category').agg({'Profit': 'sum'}).reset_index()
                                   .sort_values(by='Profit', ascending=False).head(3))
                sub_category_profit = (filtered_df.groupby('Sub-Category').agg({'Profit': 'sum'}).reset_index()
                                       .sort_values(by='Profit', ascending=False).head(5))

                # Display top 5 profitable markets, countries, categories, sub-categories, and customers
                col1, col2 = st.columns(2)

                with col1:
                    st.write("Top 5 **Markets** by Profit:")
                    st.dataframe(market_profit, width=350)

                    st.write("Top 5 **Countries** by Profit:")
                    st.dataframe(country_profit, width=350)

                with col2:
                    st.write("Top 5 **Sub-Categories** by Profit:")
                    st.dataframe(sub_category_profit, width=350)

                    st.write("Top 3 **Categories** by Profit:")
                    st.dataframe(category_profit, width=350)

                # Visualizations
                st.subheader("Data Visualization")

                # Profit by Market
                profit_by_market_chart = alt.Chart(market_profit).mark_bar().encode(
                    x=alt.X('Market:O', sort='-y', title='Market'),
                    y=alt.Y('Profit:Q', title='Total Profit'),
                    color=alt.Color('Market:N', legend=None, scale=alt.Scale(scheme='paired')),
                    tooltip=['Market', 'Profit']
                ).properties(
                    width=600,
                    height=400,
                    title=alt.Title("Total Profit by Market", fontWeight="bolder")

                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14
                ).configure_title(
                    fontSize=16
                ).configure_view(
                    strokeOpacity=0
                )

                st.altair_chart(profit_by_market_chart, use_container_width=True)

                # Profit by Country
                profit_by_country_chart = alt.Chart(country_profit).mark_bar().encode(
                    x=alt.X('Country:O', sort='-y', title='Country'),
                    y=alt.Y('Profit:Q', title='Total Profit'),
                    color=alt.Color('Country:N', legend=None, scale=alt.Scale(scheme='paired')),
                    tooltip=['Country', 'Profit']
                ).properties(
                    width=600,
                    height=400,
                    title=alt.Title("Total Profit by Country", fontWeight="bolder")
                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14
                ).configure_title(
                    fontSize=16
                ).configure_view(
                    strokeOpacity=0
                )

                st.altair_chart(profit_by_country_chart, use_container_width=True)

                # Profit by Category
                profit_by_category_chart = alt.Chart(category_profit).mark_bar().encode(
                    x=alt.X('Category:O', sort='-y', title='Category'),
                    y=alt.Y('Profit:Q', title='Total Profit'),
                    color=alt.Color('Category:N', legend=None, scale=alt.Scale(scheme='paired')),
                    tooltip=['Category', 'Profit']
                ).properties(
                    width=600,
                    height=400,
                    title=alt.Title("Total Profit by Category", fontWeight="bolder")
                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14
                ).configure_title(
                    fontSize=16
                ).configure_view(
                    strokeOpacity=0
                )

                st.altair_chart(profit_by_category_chart, use_container_width=True)

                # Profit by Sub-Category
                profit_by_sub_category_chart = alt.Chart(sub_category_profit).mark_bar().encode(
                    x=alt.X('Sub-Category:O', sort='-y', title='Sub-Category'),
                    y=alt.Y('Profit:Q', title='Total Profit'),
                    color=alt.Color('Sub-Category:N', legend=None, scale=alt.Scale(scheme='paired')),
                    tooltip=['Sub-Category', 'Profit']
                ).properties(
                    width=600,
                    height=400,
                    title=alt.Title("Total Profit by Sub-Category", fontWeight="bolder")
                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14
                ).configure_title(
                    fontSize=16
                ).configure_view(
                    strokeOpacity=0
                )

                st.altair_chart(profit_by_sub_category_chart, use_container_width=True)


        else:
            st.warning("No profitability data available with current filter applied.", icon="⚠️")

    else:
        st.warning("No data available. Please upload a dataset.")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            try:
                st.session_state.df = pd.read_csv(uploaded_file)
                st.success("File uploaded successfully!")
            except Exception as e:
                st.error(f"Error uploading file: {e}")


class ProfitScenario:
    def __init__(self):
        pass


# Initialize and run the app
if __name__ == "__main__":
    scenario = ProfitScenario()
    scenario.profit_logic = profit_logic
    scenario.profit_logic()
