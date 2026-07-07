# Defines internal application logic
import streamlit as st
import bs4
import js2py
import requests
from typing import Union


# Func: Fetch edcaps calculator (JS directly embedded in HTML)
# Use streamlit cache to only refresh the HTML calculator form once per week
# @st.cache_data()
def fetch_edcaps_HTML():
    ...


# Func: Extract HTML Form - Repayment Calculator
def extract_calc_HTML_form():
    ...


# Func: Extract JS logic - Repayment Calculator
def extract_calc_JS_logic():
    ...


def calculate_edcap_results():
    # Take user inputs from streamlit
    # Use inputs in edcaps calculator
    # Submit and retrieve results
    # Return all results
    return ["trad", "ibr", "icr", "paye", "rap"]


def calculate_REPAYE_plan():
    # Take necessary user inputs
    # Calculate REPAYE monthly payment plan amount
    # Return result
    return ["repaye"]


# Func: Streamlit User Inputs (defined by edcaps form params)
#           -> ([IDR Plans], Traditional Payment Plan) monthly payment amounts
def display_diff(display_value: str, *, percent_diff: float) -> None:
    # If the percent difference is greater than or equal to 20% in either direction
    # Mark red, known as a "flagged difference"
    # Nicely formated as +-$
    # This: +$200 and -$200
    # Instead of: $200 and $-200
    if abs(percent_diff) >= 0.2:
        with st.container(key="metric-card"):
            if percent_diff > 0:
                display_value = display_value.replace("$", "+$").replace("(", "(+")
            else:
                display_value = display_value.replace("$", "-$")

            st.metric("**Total Difference**", value=display_value, border=True)
    else:
        st.metric("**Total Difference**", value=display_value, border=True)


def calculate_comparisons() -> None:
    trad, ibr, icr, paye, rap = calculate_edcap_results()
    repaye = calculate_REPAYE_plan()

    user_reported_est = 350
    selected_plan = st.session_state.servicer_estimate  # TODO: Use something to correspond selected_plan to this, probably case statement or dict
    est_difference = user_reported_est - selected_plan
    est_percent_diff = (est_difference) / selected_plan

    display_diff(f"${abs(est_difference)} ({est_percent_diff:0,.0%})", percent_diff=est_percent_diff)


# Func: Create popup if there is a flagged difference
# TODO: Make sure it pops-up only once per session (How?)
# NOTE: Maybe make this a button, so instead of worrying about implementation, users can opt-in to share