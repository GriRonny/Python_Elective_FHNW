import streamlit as st
import pandas as pd
import numpy as np

import main_dashboard


class SalesScenario:
    def __init__(self):
        pass

    def sales_logic(self):
        st.header("Sales Section")

        if st.session_state.df is not None:  # Checking if session state df is not empty
            df = st.session_state.df  # assigning session state df to variable "df"

            st.bar_chart(data=df["Sales"])

        if st.button("Go back to Analysis"):
            main_dashboard.switch_view('analysis')