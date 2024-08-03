import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


def profit_logic():
    st.header("Profitability Section")

    if st.session_state.df is not None:  # Checking if session state df is not empty
        df = st.session_state.df  # assigning session state df to variable "df"

        st.write(df)

    else:
        st.error("No data loaded. Please upload a CSV file.")

    with st.sidebar:
        if st.button("Return to overview"):
            st.session_state.switch_view('analysis')


class ProfitScenario:
    def __init__(self):
        pass
