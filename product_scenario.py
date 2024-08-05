import streamlit as st
import pandas as pd
import altair as alt


class ProductScenario:
    def __init__(self):  # Empty constructor
        pass

    def product_logic(self):
        st.header("Product Analytics")

        # Error Handling here? Because data might be empty?
        if 'df' in st.session_state and st.session_state.df is not None:  # Checking if session state df is not empty
            df = st.session_state.df  # Assigning session state df to variable "df"

            # Ensure numeric columns are of correct type
            df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
            df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
            df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce')
            df['Shipping Cost'] = pd.to_numeric(df['Shipping Cost'], errors='coerce')

            # Ensure 'Order Date' is datetime
            df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d %m %Y', errors='coerce')

            # Remove rows with missing Order Dates
            df = df.dropna(subset=['Order Date'])

            # Sidebar for Product Category Filter
            with st.sidebar:
                st.header("Please Filter Here")

                st.subheader("Filter by Product Category")
                categories = df['Category'].unique()
                selected_category = st.multiselect("Select Category", categories)

                # Filter DataFrame by selected categories before showing sub-categories
                if selected_category:
                    df = df[df['Category'].isin(selected_category)]

                st.subheader("Filter by Sub-Category")
                sub_categories = df['Sub-Category'].unique()
                selected_sub_category = st.multiselect("Select Sub-Category", sub_categories)

                # Filter DataFrame by selected sub-categories before showing years
                if selected_sub_category:
                    df = df[df['Sub-Category'].isin(selected_sub_category)]

                st.subheader('Select relevant year')
                df['Order Year'] = df['Order Date'].dt.year
                unique_years = df['Order Year'].dropna().unique()
                year_select = st.sidebar.multiselect('Select Year', options=unique_years)

                if year_select:
                    df = df[df['Order Year'].isin(year_select)]

            # Top-Selling Products & Least-Selling Products
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top-Selling Products")
                top_selling = df.groupby('Product Name').sum(numeric_only=True)['Sales'].sort_values(
                    ascending=False).head(10).reset_index()
                if not top_selling.empty:
                    top_selling['Rank'] = top_selling['Sales'].rank(method='first', ascending=False)
                    chart = alt.Chart(top_selling).mark_bar().encode(
                        x=alt.X('Sales:Q', title='Sales'),
                        y=alt.Y('Product Name:N', sort='-x', title='Product Name'),
                        color=alt.Color('Rank:Q', scale=alt.Scale(domain=[1, 10], range=['darkgreen', 'lightgreen']),
                                        legend=None),
                        tooltip=['Product Name', 'Sales']
                    ).properties(
                        width=350,
                        height=400
                    )
                    st.altair_chart(chart)
                else:
                    st.write("No data available for Top-Selling Products.")

            with col2:
                st.subheader("Least-Selling Products")
                least_selling = df.groupby('Product Name').sum(numeric_only=True)['Sales'].sort_values().head(
                    10).reset_index()
                if not least_selling.empty:
                    least_selling['Rank'] = least_selling['Sales'].rank(method='first', ascending=True)
                    chart = alt.Chart(least_selling).mark_bar().encode(
                        x=alt.X('Sales:Q', title='Sales'),
                        y=alt.Y('Product Name:N', sort='-x', title='Product Name'),
                        color=alt.Color('Rank:Q', scale=alt.Scale(domain=[1, 10], range=['darkred', 'lightcoral']),
                                        legend=None),
                        tooltip=['Product Name', 'Sales']
                    ).properties(
                        width=350,
                        height=400
                    )
                    st.altair_chart(chart)
                else:
                    st.write("No data available for Least-Selling Products.")

            # Sales Trends Over Time
            st.subheader("Sales Trends Over Time")
            sales_trends = df.resample('M', on='Order Date').sum(numeric_only=True)['Sales'].reset_index()
            if not sales_trends.empty:
                sales_trends['Order Date'] = pd.to_datetime(sales_trends['Order Date'])
                brush = alt.selection_interval(encodings=['x'])

                base = alt.Chart(sales_trends).mark_line(point=True).encode(
                    x=alt.X('Order Date:T', title='Date'),
                    y=alt.Y('Sales:Q', title='Sales'),
                    tooltip=['Order Date:T', 'Sales:Q']
                ).properties(
                    width=700,
                    height=400
                ).add_selection(
                    brush
                )

                trendline = base.transform_regression('Order Date', 'Sales').mark_line(color='red', strokeDash=[5, 5])
                st.altair_chart(base + trendline)
            else:
                st.write("No data available for Sales Trends Over Time.")

            # Sales by Product Category & Sales by Sub-Category
            col3, col4 = st.columns(2)
            with col3:
                st.subheader("Sales by Product Category")
                sales_by_category = df.groupby('Category').sum(numeric_only=True)['Sales'].sort_values(
                    ascending=False).reset_index()
                if not sales_by_category.empty:
                    sales_by_category['Percentage'] = sales_by_category['Sales'] / sales_by_category[
                        'Sales'].sum() * 100
                    sales_by_category['Category'] = sales_by_category['Category'].astype(str)

                    chart = alt.Chart(sales_by_category).mark_arc(innerRadius=50).encode(
                        theta=alt.Theta(field="Percentage", type="quantitative"),
                        color=alt.Color(field="Category", type="nominal"),
                        tooltip=['Category', 'Sales', 'Percentage']
                    ).properties(
                        width=350,
                        height=400
                    )
                    st.altair_chart(chart)
                else:
                    st.write("No data available for Sales by Product Category.")

            with col4:
                st.subheader("Sales by Sub-Category")
                sales_by_sub_category = df.groupby('Sub-Category').sum(numeric_only=True)['Sales'].sort_values(
                    ascending=False).reset_index()
                if not sales_by_sub_category.empty:
                    chart = alt.Chart(sales_by_sub_category).mark_bar().encode(
                        x=alt.X('Sales:Q', title='Sales'),
                        y=alt.Y('Sub-Category:N', sort='-x', title='Sub-Category'),
                        tooltip=['Sub-Category', 'Sales']
                    ).properties(
                        width=350,
                        height=400
                    )
                    st.altair_chart(chart)
                else:
                    st.write("No data available for Sales by Sub-Category.")

            # Profit by Product Category & Profit by Sub-Category
            col5, col6 = st.columns(2)
            with col5:
                st.subheader("Profit by Product Category")
                profit_by_category = df.groupby('Category').sum(numeric_only=True)['Profit'].sort_values(
                    ascending=False).reset_index()
                if not profit_by_category.empty:
                    profit_by_category['Percentage'] = profit_by_category['Profit'] / profit_by_category[
                        'Profit'].sum() * 100
                    profit_by_category['Category'] = profit_by_category['Category'].astype(str)

                    chart = alt.Chart(profit_by_category).mark_arc(innerRadius=50).encode(
                        theta=alt.Theta(field="Percentage", type="quantitative"),
                        color=alt.Color(field="Category", type="nominal"),
                        tooltip=['Category', 'Profit', 'Percentage']
                    ).properties(
                        width=350,
                        height=400
                    )
                    st.altair_chart(chart)
                else:
                    st.write("No data available for Profit by Product Category.")

            with col6:
                st.subheader("Profit by Sub-Category")
                profit_by_sub_category = df.groupby('Sub-Category').sum(numeric_only=True)['Profit'].sort_values(
                    ascending=False).reset_index()
                if not profit_by_sub_category.empty:
                    chart = alt.Chart(profit_by_sub_category).mark_bar().encode(
                        x=alt.X('Profit:Q', title='Profit'),
                        y=alt.Y('Sub-Category:N', sort='-x', title='Sub-Category'),
                        tooltip=['Sub-Category', 'Profit']
                    ).properties(
                        width=350,
                        height=400
                    )
                    st.altair_chart(chart)
                else:
                    st.write("No data available for Profit by Sub-Category.")

            # Average Discount by Category & Average Discount by Sub-Category
            col7, col8 = st.columns(2)
            with col7:
                st.subheader("Average Discount by Category")
                avg_discount_by_category = df.groupby('Category').mean(numeric_only=True)['Discount'].sort_values(
                    ascending=False).reset_index()
                if not avg_discount_by_category.empty:
                    avg_discount_by_category['Percentage'] = avg_discount_by_category['Discount'] / \
                                                             avg_discount_by_category['Discount'].sum() * 100

                    avg_discount_by_category['Category'] = avg_discount_by_category['Category'].astype(str)

                    chart = alt.Chart(avg_discount_by_category).mark_arc(innerRadius=50).encode(
                        theta=alt.Theta(field="Percentage", type="quantitative"),
                        color=alt.Color(field="Category", type="nominal"),
                        tooltip=['Category', 'Discount', 'Percentage']
                    ).properties(
                        width=350,
                        height=400
                    )
                    st.altair_chart(chart)
                else:
                    st.write("No data available for Average Discount by Category.")

            with col8:
                st.subheader("Average Discount by Sub-Category")
                avg_discount_by_sub_category = df.groupby('Sub-Category').mean(numeric_only=True)['Discount'].sort_values(ascending=False).reset_index()
                if not avg_discount_by_sub_category.empty:
                    chart = alt.Chart(avg_discount_by_sub_category).mark_bar().encode(
                        x=alt.X('Discount:Q', title='Average Discount'),
                        y=alt.Y('Sub-Category:N', sort='-x', title='Sub-Category'),
                        tooltip=['Sub-Category', 'Discount']
                    ).properties(
                        width=350,
                        height=400
                    )
                    st.altair_chart(chart)
                else:
                    st.write("No data available for Average Discount by Sub-Category.")

            # Shipping Cost Analysis by Category & Shipping Cost Analysis by Sub-Category
            col9, col10 = st.columns(2)
            with col9:
                st.subheader("Shipping Cost Analysis by Category")
                shipping_cost_by_category = df.groupby('Category').mean(numeric_only=True)['Shipping Cost'].sort_values(ascending=False).reset_index()
                if not shipping_cost_by_category.empty:
                    shipping_cost_by_category['Percentage'] = shipping_cost_by_category['Shipping Cost'] / shipping_cost_by_category['Shipping Cost'].sum() * 100
                    shipping_cost_by_category['Category'] = shipping_cost_by_category['Category'].astype(str)

                    chart = alt.Chart(shipping_cost_by_category).mark_arc(innerRadius=50).encode(
                        theta=alt.Theta(field="Percentage", type="quantitative"),
                        color=alt.Color(field="Category", type="nominal"),
                        tooltip=['Category', 'Shipping Cost', 'Percentage']
                    ).properties(
                        width=350,
                        height=400
                    )
                    st.altair_chart(chart)
                else:
                    st.write("No data available for Shipping Cost by Category.")

            with col10:
                st.subheader("Shipping Cost Analysis by Sub-Category")
                shipping_cost_by_sub_category = df.groupby('Sub-Category').mean(numeric_only=True)['Shipping Cost'].sort_values(ascending=False).reset_index()
                if not shipping_cost_by_sub_category.empty:
                    chart = alt.Chart(shipping_cost_by_sub_category).mark_bar().encode(
                        x=alt.X('Shipping Cost:Q', title='Shipping Cost'),
                        y=alt.Y('Sub-Category:N', sort='-x', title='Sub-Category'),
                        tooltip=['Sub-Category', 'Shipping Cost']
                    ).properties(
                        width=350,
                        height=400
                    )
                    st.altair_chart(chart)
                else:
                    st.write("No data available for Shipping Cost by Sub-Category.")

        else:
            st.error("No data loaded. Please upload a CSV file.")

        with st.sidebar:
            if st.button("Return to overview"):
                st.session_state.switch_view('analysis')
