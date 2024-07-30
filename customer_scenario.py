import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt


def create_age_column():
    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # assigning session state df to variable "df"

        # Calculating the age of the customers

        # Convert 'Date of Birth' column to datetime format
        df['Customer DOB'] = pd.to_datetime(df['Customer DOB'])

        # Calculate the current date
        current_date = pd.to_datetime('today')

        # Handle the missing date of birth cels and make them age 0
        df['Customer DOB'].fillna(pd.to_datetime(current_date), inplace=True)

        # Calculating the age --> used ChatGPT to come up with this idea
        df['Age'] = df['Customer DOB'].apply(
            lambda dob: current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day)))

        df['Age'] = df['Age'].astype(int)

        age_range = df['Age']

        return age_range


def customer_logic():
    st.header("Customer Analyses")

    # Error Handling here? Because data might be empty?

    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # assigning session state df to variable "df"

        # Filter the DataFrame for the segment "Customer" to get the min age for the warning display
        min_df = df[df['Segment'] == 'Consumer']

        # Find the minimum age within the filtered DataFrame
        min_age_customer = min_df['Age'].min()

        # Sidebar for Segment Filter
        with st.sidebar:
            st.header("Please Filter Here")
            st.subheader("Filter by Customer Segment")
            seg_type = df['Segment'].unique()
            selected_seg = [st.checkbox(segment, key=segment) for segment in seg_type]

        # Create lists of selected segments
        selected_segment_list = [segment for segment, selected in zip(seg_type, selected_seg) if selected]

        # Create sidebar menu for gender selection
        with st.sidebar:
            st.subheader("Filter Gender")
            gender_type = [g_type for g_type in df['Gender'].unique()]
            selected_gender = [st.checkbox(gender, key=gender) for gender in gender_type]

        # Create lists of selected gender
        selected_gender_list = [gender for gender, selected in zip(gender_type, selected_gender) if selected]

        with st.sidebar:
            st.subheader("Filter Age Range")
            # Check if corporate checkbox is selected (Maybe different way possible?)
            if selected_seg[1]:
                st.info('Note: Corporate customers have their age set to 0.', icon="ℹ️")
            age_slider = st.slider("Age Range ", min_value=min(create_age_column()), max_value=max(create_age_column()),
                                   value=(min(create_age_column()), max(create_age_column())))

        # Store min and max values from slider in variables
        selected_min_age, selected_max_age = age_slider

        # sidebar menu to select years
        with st.sidebar.subheader('Select relevant year'):
            # Ensure the sales date column is in datetime format
            df['Order Date'] = pd.to_datetime(df['Order Date'])

            # Extract the year from the sales date
            df['Order Year'] = df['Order Date'].dt.year

            # Get unique sales years
            unique_years = df['Order Year'].unique()

            # create sidebar selection with the years
            year_select = st.sidebar.multiselect('Select Year', options=unique_years)

        # Prefilter the data based on the selected Age range via the age_slider!
        df = df[(df['Age'] >= selected_min_age) & (df['Age'] <= selected_max_age)]

        # Filter the DataFrame based on selected segment, year, and gender
        if selected_segment_list and year_select and selected_gender_list:
            filtered_df = df[
                (df['Segment'].isin(selected_segment_list) & df['Order Year'].isin(year_select)
                 & df['Gender'].isin(selected_gender_list))
            ]

        elif selected_segment_list and year_select:
            filtered_df = df[
                (df['Segment'].isin(selected_segment_list) & df['Order Year'].isin(year_select))
            ]

        elif selected_segment_list and selected_gender_list:
            filtered_df = df[
                (df['Segment'].isin(selected_segment_list) & df['Gender'].isin(selected_gender_list))
            ]

        elif selected_gender_list and year_select:
            filtered_df = df[
                (df['Order Year'].isin(year_select)
                 & df['Gender'].isin(selected_gender_list))
            ]

        elif selected_segment_list:
            filtered_df = df[df['Segment'].isin(selected_segment_list)]

        elif year_select:
            filtered_df = df[df['Order Year'].isin(year_select)]

        elif selected_gender_list:
            filtered_df = df[df['Gender'].isin(selected_gender_list)]

        else:
            filtered_df = df  # If no filters selected, use original/unfiltered df

        payment_counts = filtered_df['Payment Method'].value_counts().reset_index()
        payment_counts.columns = ['Payment Method', 'Count']

        # Code to identify best customers
        most_profitable_cus = filtered_df.groupby('Customer Name')['Profit'].sum().reset_index()
        top_profitable_cus = most_profitable_cus.sort_values(by='Profit', ascending=False).head(5)

        # Code to identify the worst customers
        least_profitable_cus = filtered_df.groupby('Customer Name')['Profit'].sum().reset_index()
        top_worst_cus = least_profitable_cus.sort_values(by='Profit', ascending=True).head(5)

        if filtered_df.empty:
            st.warning(f"Age filter set to low. The min age for consumer segment is {min_age_customer} :warning:", icon='⚠️')

        else:
            # Displaying best and worst customers
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Most profitable customers:+1:")
                st.write(top_profitable_cus)

            with col2:
                st.subheader("Least profitable customers:-1:")
                st.write(top_worst_cus)

            # Add a title above the bar chart
            st.subheader("Favored payment method of all customers :credit_card:")

            col3, col4 = st.columns(2)
            with col3:
                # Display the bar chart
                st.bar_chart(payment_counts.set_index('Payment Method'))

            with col4:
                # Display a pie chart of to visualize the payment method distribution
                fig, ax = plt.subplots()
                ax.pie(payment_counts['Count'], labels=payment_counts['Payment Method'], autopct='%1.1f%%',
                       startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                # Display the pie chart in Streamlit
                st.pyplot(fig)

    else:
        st.error("No data loaded. Please upload a CSV file.")

    with st.sidebar:
        if st.button("Return to overview"):
            st.session_state.switch_view('analysis')


class CustomerScenario:
    def __init__(self):  # Empty constructor
        pass
