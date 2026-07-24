# Defines application UI layout and content
# ref: https://www.youtube.com/watch?v=c8QXUrvSSyg
import streamlit as st
import calculator as calc

def init_session_state() -> None:
    defaults = {
        "servicer_estimate": 0.0,
        "total_balance": 0.0,
        "annual_interest_rate": 0.0,
        "agi": 0.0,
        "household_size": 0,
        "num_of_dependents": 0,
        "state_of_residency": "Contiguous U.S.",
        "borrower_type": None,

        "ibr": 0.0,
        "icr": 0.0,
        "paye": 0.0,
        "repaye": 0.0,
        "rap": 0.0,
        "std": 0.0,

        "comparison_plan": "Traditional Repayment Plan",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def configure_page() -> None:
    st.set_page_config(
        page_title="Debt Collective Loan Repayment Calculator",
        layout="wide")
    st.logo("https://wordpress-cdn-prod.debtcollective.org/wp-content/uploads/2021/08/24080706/logo-black-1.png",
            size="large", link="https://debtcollective.org/")


def configure_page_title() -> None:
    # TODO: Add Debt Collective Style banner
    # I need a designer's help lol
    # st.html("""
    #     <style>
    #         .st-key-title-banner {
    #             background: #dc3545 !important;  /* Bootstrap red */
    #             color: white;
    #             width: 100%;
    #         }
    #     </style>
    # """)
    # with st.container(key="title-banner"):
    #     st.markdown("# Debt Collective Loan Repayment Calculator")

    st.markdown("## Are your servicer's monthly repayment estimates WAY off from what they should be?")
    st.subheader("A tool built *by* debtors, *for* debtors.")
    st.caption("Built with :heart: by **Marisol Yake** as part of the **Debt Collective's Payments Pause Campaign Data Team**.")
    st.markdown("This is a calculator to help debtors determine how far off their student loan servicer's estimates are from what they should be.")
    st.markdown("Uses the trustworthy process of the [EDCAP calculator](https://www.edcapny.org/resources-for-borrowers/repayment-plan-calculator/), and your estimated repayment amount, to describe exactly **how far** off.")


# Inputs get stored as st.session_state.key
def configure_input_sidebar() -> None:
    with st.sidebar:
        # Using a streamlit form prevents calculations from happening automatically
        # This prevents unnecessary computations and makes intended-use clearer
        with st.form(key="input_form"):
            # Accepts all user inputs for loan repayment calculations
            st.number_input("Servicer Monthly Payment Estimate ($):",
                            min_value=0.0, value=0.0, step=1.0,
                            key="servicer_estimate")
            st.number_input("Total Loan Balance ($):",
                            min_value=0.0, value=0.0, step=1.0,
                            key="total_balance")
            st.number_input("Annual Interest Rate (%):",
                            min_value=0.0, value=0.0, step=1.0,
                            key="annual_interest_rate")
            st.number_input("Adjusted Gross Income (AGI) ($):",
                            min_value=0.0, value=0.0, step=1.0,
                            key="agi")
            st.number_input("Household Size (For IBR, PAYE, and ICR):",
                            min_value=0, value=0, step=1,
                            key="household_size")
            st.number_input("Number of Dependents (Claimed on taxes - Only For RAP):",
                            min_value=0, value=0, step=1,
                            key="num_of_dependents")
            st.selectbox("State of Residency:",
                        options=["Contiguous U.S.", "Alaska", "Hawaii"],
                        key="state_of_residency")
            st.selectbox("Borrower Type (for IBR):",
                        options=["New Borrower (After July 1, 2014)", "Old Borrower (Before July 1, 2014)"],
                        index=None, placeholder="Choose a Borrower Type", key="borrower_type")

            submitted = st.form_submit_button("Calculate", width="stretch", type="primary")

            # After form button is hit, run calculate_all_plans()
            if submitted:
                states_dict = {
                    "Contiguous U.S.": "contiguous",
                    "Alaska": "alaska",
                    "Hawaii": "hawaii"
                }

                balance = st.session_state.total_balance
                interest = st.session_state.annual_interest_rate
                agi = st.session_state.agi
                household_size = st.session_state.household_size
                num_of_dependents = st.session_state.num_of_dependents
                state = states_dict.get(st.session_state.state_of_residency, "contiguous")
                borrower_type = "new" if "new" in str(st.session_state.borrower_type).lower() else "old"

                # TODO: Refactor so not every plan is calculated all at once
                # Please forgive me, I'm in a hurry
                st.session_state.ibr, st.session_state.icr, st.session_state.paye, st.session_state.repaye, st.session_state.rap, st.session_state.std = calc.calculate_all_plans(
                    balance=balance,
                    interest=interest,
                    agi=agi,
                    household_size=household_size,
                    num_of_dependents=num_of_dependents,
                    state=state,
                    borrower_type=borrower_type
                )


def configure_plan_selection_menu() -> None:
    st.selectbox("Payment Plan for Comparison:",
                 options=["Traditional Repayment Plan", "Income-Based Repayment (IBR)",
                 "Income-Contingent Repayment (ICR)", "Pay As You Earn (PAYE)",
                 "Revised Pay As You Earn (REPAYE)", "Repayment Assistance Plan (RAP)"],
                 index=None, placeholder="Choose a Repayment Plan", key="comparison_plan")


# Display Comparison: Loan Servicer Estimate - Repayment Plan Estimate
def display_plan_comparison():
    st.html("""
        <style>
            /* Color flagged differences as red */
            .st-key-metric-card [data-testid="stMetricValue"] {
                color: #dc3545 !important;
            }
        </style>
    """)

    plans = {
        "Income-Based Repayment (IBR)": st.session_state.ibr,
        "Income-Contingent Repayment (ICR)": st.session_state.icr,
        "Pay As You Earn (PAYE)": st.session_state.paye,
        "Revised Pay As You Earn (REPAYE)": st.session_state.repaye,
        "Repayment Assistance Plan (RAP)": st.session_state.rap,
        "Traditional Repayment Plan": st.session_state.std
    }


    col1, col2 = st.columns(2)
    with col1:
        st.metric("**Your Loan Servicer's Provided Monthly Payment Estimate**",
                  value=f"{st.session_state.servicer_estimate}",
                  format="dollar", border=True)

    with col2:
        # Provide a sensible default
        plan = st.session_state.get("comparison_plan", "Traditional Repayment Plan")

        if plan not in plans:
            plan = "Traditional Repayment Plan"

        selected_plan_amt = plans[plan]
        st.metric(f"**Monthly Payment Estimate under {plan}**",
                  value=f"{selected_plan_amt}", format="dollar", border=True)

    servicer_amt = st.session_state.servicer_estimate
    difference = servicer_amt - selected_plan_amt

    # Handles edge cases where comparison is 0 / 0
    if selected_plan_amt == 0:
        # Case 1: Where selected plan payment amount = 0 and servicer estimate = 0
        if servicer_amt == 0:
            percent_diff = 0.0
        # Case 2: Where selected plan payment amount = 0 and servicer estimate != 0
        else:
            percent_diff = 1.0  
    else:
        # Case 3: Both estimates are not equal to 0
        percent_diff = difference / selected_plan_amt


    # If the percent difference is greater than or equal to 20% in either direction
    # Mark red, known as a "flagged difference"
    # Nicely formated as +-$
    # This: +$200 and -$200
    # Instead of: $200 and $-200
    display_value = f"${abs(difference):0,.2f} ({percent_diff:0,.0%})"
    # TODO: def display_flagged_diff(display_value: string, *, percent_diff: float) -> None
    # Example use: display_flagged_diff(display_value, percent_diff=percent_diff)
    if abs(percent_diff) >= 0.2:
        with st.container(key="metric-card"):
            if percent_diff > 0:
                display_value = display_value.replace("$", "+$").replace("(", "(+")
            else:
                display_value = display_value.replace("$", "-$")

            st.metric("**Total Difference**", value=display_value, border=True)
    else:
        st.metric("**Total Difference**", value=display_value, border=True)


def configure_footer() -> None:
    st.divider()
    st.markdown("**Disclaimers**")
    disclaimers = """
        - All numbers provided are estimates.
        - Another cool disclaimer.
        - Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        - Excepteur sint occaecat cupidatat non proident.
    """
    st.caption(disclaimers)


def main() -> None:
    init_session_state()
    configure_page()
    configure_page_title()
    configure_input_sidebar()
    configure_plan_selection_menu()
    display_plan_comparison()
    configure_footer()


if __name__=="__main__":
    main()