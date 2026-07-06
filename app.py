# Defines application UI layout and content
# ref: https://www.youtube.com/watch?v=c8QXUrvSSyg
import streamlit as st


def configure_page() -> None:
    st.set_page_config(
        page_title="Debt Collective Loan Repayment Calculator",
        initial_sidebar_state="locked",
        layout="wide")


def configure_result_title() -> None:
    st.markdown("## Are your servicer's monthly repayment estimates WAY off from what they should be?")
    st.markdown("This is a calculator to help debtors determine how far off their student loan servicer's estimates are from what they should be.")
    st.markdown("Uses the trustworthy process of the [edcap calculator](https://www.edcapny.org/resources-for-borrowers/repayment-plan-calculator/), and your estimated repayment amount, to describe exactly **how far** off.")


def configure_input_sidebar() -> None:
    with st.sidebar:
        st.number_input("Servicer Monthly Payment Estimate ($):", value=0.0, key="servicer_estimate")
        st.number_input("Total Loan Balance ($):", value=0.0, key="total_balance")
        st.number_input("Annual Interest Rate (%):", value=0.0, key="annual_interest_rate")
        st.number_input("Adjusted Gross Income (AGI) ($):", value=0.0, key="agi")
        st.number_input("Household Size (For IBR, PAYE, and ICR):", value=0, key="household_size")
        st.number_input("Number of Dependents (Claimed on taxes - Only For RAP):", value=0, key="num_of_dependents")
        st.selectbox("State of Residency:", options=["Contiguous U.S.", "Alaska", "Hawaii"], key="state_of_residency")
        st.selectbox("Borrower Type (for IBR):", options=["New Borrower (After July 1, 2014)", "Old Borrower (Before July 1, 2014)"], key="borrower_type")
        # Add on_click: configure_calculator_results()
        st.button("Calculate", width="stretch")


def configure_calculator_results():
    # TODO: Externalize into CSS stylesheet 
    st.html("""
                    <style>
                        /* Color flagged differences as red */
                        .st-key-metric-card [data-testid="stMetricValue"] {
                            color: #dc3545 !important;  /* Bootstrap red */
                        }
                    </style>
                    """)
    # Placeholder variables
    # TODO: Extract this logic to engine.py
    trad_plan_est = 350.0
    placeholder_difference = st.session_state.servicer_estimate - trad_plan_est
    placeholder_percent_diff = (placeholder_difference) / trad_plan_est

    # Add spacer from intro text - visual breathing room
    st.html("<div style='height: 15px;'></div>")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("**Your Loan Servicer's Provided Monthly Payment Estimate**", value=f"{st.session_state.servicer_estimate}", format="dollar", border=True)

    with col2:
        st.metric("**Monthly Payment Estimate on the Traditional Plan**", value=f"{trad_plan_est}", format="dollar", border=True)

    # If the percent difference is greater than or equal to 20% in either direction
    # Mark red, known as a "flagged difference"
    if abs(placeholder_percent_diff) >= 0.2:
        with st.container(key="metric-card"):
            # Nicely formated as +-$
            # This: +$200 and -$200
            # Instead of: $200 and $-200
            if placeholder_percent_diff > 0:
                display_value = f"+${placeholder_difference} (+{placeholder_percent_diff:0,.0%})"
            else:
                display_value = f"-${abs(placeholder_difference)} ({placeholder_percent_diff:0,.0%})"
            st.metric("**Total Difference**", value=f"{display_value}", border=True)
    else:
        st.metric("**Total Difference**", value=f"${placeholder_difference} ({placeholder_percent_diff:0,.0%})", border=True)


def main() -> None:
    configure_page()
    configure_result_title()
    configure_input_sidebar()
    configure_calculator_results()


if __name__=="__main__":
    main()