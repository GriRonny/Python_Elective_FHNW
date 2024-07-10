import streamlit as st
import pandas as pd


def load_csv(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None


# Initialize session state
if 'view' not in st.session_state:
    st.session_state.view = 'upload'


# Function to switch view
def switch_view(view_name):
    st.session_state.view = view_name
    st.rerun()  # Trigger rerun everytime function is called to update view accordingly.


if st.session_state.view == 'upload':  # Here we display the "Upload" view if the session state == "upload"
    st.header("Upload CSV file")
    uploaded_csv = st.file_uploader("Choose a CSV file to be processed.", type="csv")

    if uploaded_csv is not None:
        df = load_csv(uploaded_csv)
        if df is not None:
            st.success("CSV file successfully loaded!")
            st.write(df)
            if st.button("Proceed to Analysis"):
                switch_view('analysis')
        else:
            st.error("Failed to load CSV file.")
    else:
        st.info("Please upload a CSV file.")
elif st.session_state.view == 'analysis':  # Here we display the "Upload" view if the session state == "analysis"
    st.header("Choose desired analysis scope")
    st.write("This is the analysis view.")

    if st.button("Go back to Upload"):  # If this button is pressed, the user returns to the defined view.
        switch_view('upload')  # switch_view function called with parameter "upload"
