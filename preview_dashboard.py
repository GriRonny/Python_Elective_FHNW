import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
from io import BytesIO

# Function to load data
def load_data(file):
    return pd.read_csv(file)

# Function to generate PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Sales Data Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, data, title):
        self.add_page()
        self.chapter_title(title)
        self.set_font('Arial', '', 12)
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.cell(40, 10, str(data[i][j]), 1, 0, 'C')
            self.ln()

def export_pdf(dataframe):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Summary Statistics')
    pdf.chapter_body(dataframe.describe().to_string())

    data = dataframe.values.tolist()
    pdf.add_table(data, 'Data')

    # Save PDF to BytesIO object
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

# Title of the dashboard
st.title("Sales Data Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = load_data(uploaded_file)

    # Display raw data
    st.header("Raw Data")
    st.write(df)

    # Summary statistics
    st.header("Summary Statistics")
    st.write(df.describe())

    # Line chart for the "Amount" column
    st.header("Amount Line Chart")
    st.line_chart(df["Amount"])

    # Histogram for the "Amount" column
    st.header("Amount Distribution")
    st.bar_chart(np.histogram(df["Amount"], bins=30)[0])

    # Pie chart for the "Region" column
    st.header("Region Distribution")
    region_counts = df['Region'].value_counts()
    st.write(region_counts)
    st.pyplot(region_counts.plot.pie(autopct="%1.1f%%").figure)

    # Scatter plot for "Price" vs "Amount"
    st.header("Price vs Amount Scatter Plot")
    st.write(df.plot.scatter(x='Price', y='Amount'))

    # Additional options
    st.sidebar.header("Options")

    # Filter data based on Amount
    amount_filter = st.sidebar.slider('Filter by Amount', min_value=int(df['Amount'].min()), max_value=int(df['Amount'].max()),
                                      value=(int(df['Amount'].min()), int(df['Amount'].max())))
    filtered_data_amount = df[(df['Amount'] >= amount_filter[0]) & (df['Amount'] <= amount_filter[1])]

    st.subheader(f"Data filtered by amount between {amount_filter[0]} and {amount_filter[1]}")
    st.write(filtered_data_amount)

    # Filter data based on Price
    price_filter = st.sidebar.slider('Filter by Price', min_value=float(df['Price'].min()), max_value=float(df['Price'].max()),
                                     value=(float(df['Price'].min()), float(df['Price'].max())))
    filtered_data_price = df[(df['Price'] >= price_filter[0]) & (df['Price'] <= price_filter[1])]

    st.subheader(f"Data filtered by price between {price_filter[0]} and {price_filter[1]}")
    st.write(filtered_data_price)

    # Button to export PDF
    if st.button('Export as PDF'):
        pdf_bytes = export_pdf(df)
        st.download_button(label="Download PDF", data=pdf_bytes, file_name="sales_data_report.pdf",
                           mime="application/pdf")
else:
    st.write("Please upload a CSV file to proceed.")
