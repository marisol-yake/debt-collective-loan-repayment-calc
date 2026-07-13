# Defines internal application logic
import streamlit as st
import bs4
import requests
import pythonmonkey as pm
import typing


class JavascriptNotFoundError(Exception):
    pass

# TODO: Wrap this in a class - EDCAPCalcFetcher
# Func: Fetch edcaps calculator (JS directly embedded in HTML)
# Use streamlit cache to only refresh the HTML calculator form once per week
# @st.cache_data()
def fetch_edcaps_HTML():
    ...

# TODO: Wrap this in a class - EDCAPCalcFetcher
# Func: Extract HTML Form - Repayment Calculator
def extract_calc_HTML_form():
    filepath = "./Repayment-Plan-Calculator-7.6.26.html"

    with open(filepath, "r", encoding="utf-8") as HTML:
        soup = bs4.BeautifulSoup(HTML, "html.parser")
        return soup

# TODO: Wrap this in a class - EDCAPCalcFetcher
# Func: Extract JS logic - Repayment Calculator
def extract_calc_JS_logic(soup: bs4.BeautifulSoup):
    try:
        calc_logic = soup.find_all("script")[0].get_text(strip=True)
        pm.eval(calc_logic)

        # Extract relevant logic from the code
        calculator_ctx = {
            "calculateStandardPayment": pm.globalThis.calculateStandardPayment,
            "calculateICR": pm.globalThis.calculateICR,
            "calculateIBR": pm.globalThis.calculateIBR,
            "calculatePAYE": pm.globalThis.calculatePAYE,
            "calculateRAP": pm.globalThis.calculateRAP,
        }

    except:
        raise JavascriptNotFoundError("Javascript logic not found. Potentially extracted the wrong HTML file or server blocked this script.")

    return calculator_ctx


# TODO: Wrap this in a class - LoanRepayCalculator
def calculateREPAYE(ibr: float):
    # Take necessary user inputs
    # Calculate REPAYE monthly payment plan amount
    # Return result
    return ibr * 0.666


# TODO: Wrap this in a class - LoanRepayCalculator
def calculate_all_plans(ctx: dict):
    # TODO: Get variables from st.session_state
    # Test variables:
    balance = 10_000
    interest = 7.34
    agi = 30_000
    household = 1
    state = "contiguous"
    dependents = 0
    borrowerType = "new"

    # Calculate loan payment amounts based on EDCAP functions
    ibr = ctx["calculateIBR"](balance, interest, agi, household, state, borrowerType).monthlyPayment
    icr = ctx["calculateICR"](balance, interest, agi, household, state).monthlyPayment
    paye = ctx["calculatePAYE"](balance, interest, agi, household, state).monthlyPayment
    repaye = calculateREPAYE(ibr)
    rap = ctx["calculateRAP"](agi, dependents).monthlyPayment
    std = ctx["calculateStandardPayment"](balance, interest, years = 10)

    print(f"{ibr=:,.2f}\n{icr=:,.2f}\n{paye=:,.2f}\n{repaye=:,.2f}\n{rap=:,.2f}\n{std=:,.2f}")
    
    return ibr, icr, paye, repaye, rap, std


# TODO: Wrap this in a class - LoanRepayCalculator
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

# TODO: Wrap this in a class - LoanRepayCalculator
def calculate_comparisons() -> None:
    # TODO: Refactor so this isn't run every time the calculation is run
    # Probably going to store soup and ctx as class attributes to share state
    soup = extract_calc_HTML_form()
    ctx = extract_calc_JS_logic(soup)
    ibr, icr, paye, repaye, rap, std = calculate_all_plans(ctx)

    user_reported_est = 350
    selected_plan = st.session_state.servicer_estimate
    est_difference = user_reported_est - selected_plan
    est_percent_diff = (est_difference) / selected_plan

    display_diff(f"${abs(est_difference)} ({est_percent_diff:0,.0%})", percent_diff=est_percent_diff)

# Func: Create popup if there is a flagged difference
# TODO: Make sure it pops-up only once per session (How?)
# NOTE: Maybe make this a button, so instead of worrying about implementation, users can opt-in to share

if __name__=="__main__":
    soup = extract_calc_HTML_form()
    ctx = extract_calc_JS_logic(soup)
    calculate_all_plans(ctx)