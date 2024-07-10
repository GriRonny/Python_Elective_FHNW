import streamlit as st
import pandas as pd


def load_csv(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None


st.header("Test")
uploaded_csv = st.file_uploader("Choose a CSV file to be processed.", type="csv")

if uploaded_csv is not None:
    df = load_csv(uploaded_csv)
    if df is not None:
        st.success("CSV file successfully loaded!")
        st.write(df)
    else:
        st.error("Failed to load CSV file.")
else:
    st.info("Please upload a CSV file.")
