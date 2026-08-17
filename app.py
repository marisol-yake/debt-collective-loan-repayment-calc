# Defines application UI layout and content
# ref: https://www.youtube.com/watch?v=c8QXUrvSSyg
import streamlit as st
import engine
import time


def init_session_state() -> None:
    defaults = {
        # Default calculator inputs
        "ibr": 0.0,
        "icr": 0.0,
        "paye": 0.0,
        "repaye": 0.0,
        "rap": 0.0,
        "save": 0.0,
        "std": 0.0,
        "total_balance": 0.0,
        "grad_loan_balance": 0.0,
        "comparison_plan": "Traditional Repayment Plan",

        # UI Behavior
        "input_checklist_timer_done": False,

        # Help Messages
        "agi_helper": """Adjusted Gross Income (**AGI**) = (**Hourly Rate** x **Hours Worked Per Week**) x **Weeks Worked In a Year**
        Example: \t**AGI** = (\$25 x 40) x 52 -> **AGI** = \$52,000
        """,
        "servicer_estimate_helper": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "household_size_helper": "Used in calculations for IBR, PAYE, and ICR",
        "state_of_residency_helper": "If you don't live in **Alaska** or **Hawaii**, you can use **Contiguous U.S.**",
        "annual_interest_rate_helper": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "num_of_dependents_helper": "Claimed on taxes. Only for RAP calculation.",
        "borrower_type_helper": "Used for IBR calculations.",
        "total_balance_helper": "Your outstanding loan balance.",
        "grad_loan_balance_helper": "Loan balance from graduate school studies."
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def init_sensible_default_for(session_state_var_name, *, value: float | int):
    if session_state_var_name is None:
        session_state_var_name = value

    return session_state_var_name


def configure_page() -> None:
    st.html(
        """
        <style>
        [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapseButton"] {
                animation: bounce 2s ease infinite;
                background: #E9ECEF;
                visibility: visible;
                border-style: solid;
                border-color: #ACADAC;
                border-width: 2.5px;
                border-radius: 10px;
            }
        @keyframes bounce {
            70% { transform:translateY(0%); }
            80% { transform:translateY(-15%); }
            90% { transform:translateY(0%); }
            95% { transform:translateY(-7%); }
            97% { transform:translateY(0%); }
            99% { transform:translateY(-3%); }
            100% { transform:translateY(0); }
        }
        </style>
        """
    )
    st.set_page_config(
        page_title="Debt Collective Loan Repayment Calculator",
        initial_sidebar_state=600,
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


def configure_input_sidebar() -> None:
    # Inputs get stored as st.session_state.key
    with st.sidebar:
        has_grad_loans = st.checkbox("Do you have graduate school loans?",
                        key="grad_school_loans_flag")

        # Using a streamlit form prevents calculations from happening automatically
        # This prevents unnecessary computations and makes intended-use clearer
        with st.form(key="input_form"):
            # Accepts all user inputs for loan repayment calculations
            # Setting value=None means that st.number_input is already cleared for users automatically.

            st.number_input("Adjusted Gross Income (AGI) ($):",
                            min_value=0.0, value=None, step=1.0, placeholder="$0.00",
                            help=st.session_state.get("agi_helper"),
                            key="agi")

            col1, col2 = st.columns(2)
            with col1:
                st.number_input("Servicer Monthly Estimate ($):",
                                min_value=0.0, value=None, step=1.0, placeholder="$0.00",
                                help=st.session_state.get("servicer_estimate_helper"),
                                key="servicer_estimate")
                st.number_input("Household Size:",
                                min_value=0, value=None, step=1, placeholder="0",
                                help=st.session_state.get("household_size_helper"),
                                key="household_size")
                st.selectbox("State of Residency:",
                             options=["Contiguous U.S.", "Alaska", "Hawaii"],
                             help=st.session_state.get("state_of_residency_helper"),
                             key="state_of_residency")

            with col2:
                st.number_input("Annual Interest Rate (%):",
                                min_value=0.0, value=None, step=1.0, placeholder="0.00%",
                                help=st.session_state.get("annual_interest_rate_helper"),
                                key="annual_interest_rate")
                st.number_input("Number of Dependents:",
                                min_value=0, value=None, step=1, placeholder="0",
                                help=st.session_state.get("num_of_dependents_helper"),
                                key="num_of_dependents")
                st.selectbox("Borrower Type:",
                             options=["New Borrower (After July 1, 2014)", "Old Borrower (Before July 1, 2014)"],
                             help=st.session_state.get("borrower_type_helper"),
                             index=None, placeholder="Choose a Borrower Type",
                             key="borrower_type")

            # Grad School Loan toggle checkbox
            # Can only loan dynamically if checkbox is not within form
            if not has_grad_loans:
                st.number_input("Total Loan Balance ($):",
                                min_value=0.0, value=None, step=1.0, placeholder="$0.00",
                                help=st.session_state.get("total_balance_helper"),
                                key="total_balance")
            else:
                st.number_input("Undergraduate Loan Balance ($):",
                                min_value=0.0, value=None, step=1.0, placeholder="$0.00",
                                help=st.session_state.get("total_balance_helper"),
                                key="total_balance")
                st.number_input("Graduate School Loan Balance ($):",
                                min_value=0.0, value=None, step=1.0, placeholder="$0.00",
                                help=st.session_state.get("grad_loan_balance_helper"),
                                key="grad_loan_balance")

            submitted = st.form_submit_button("Calculate", width="stretch", type="primary")

            # After form button is hit, run calculate_all_plans()
            if submitted:
                states_dict = {
                    "Contiguous U.S.": "contiguous",
                    "Alaska": "alaska",
                    "Hawaii": "hawaii"
                }

                balance = init_sensible_default_for(st.session_state.total_balance, value=0.0)
                grad_loan_balance = init_sensible_default_for(st.session_state.grad_loan_balance, value=0.0)
                interest = init_sensible_default_for(st.session_state.annual_interest_rate, value=0.0)
                agi = init_sensible_default_for(st.session_state.agi, value=0.0)
                household_size = init_sensible_default_for(st.session_state.household_size, value=0)
                num_of_dependents = init_sensible_default_for(st.session_state.num_of_dependents, value=0)
                state = states_dict.get(st.session_state.state_of_residency, "contiguous")
                borrower_type = "new" if "new" in str(st.session_state.borrower_type).lower() else "old"

                # TODO: Refactor so not every plan is calculated all at once
                # Please forgive me, I'm in a hurry
                st.session_state.ibr, st.session_state.icr, st.session_state.paye, st.session_state.repaye, st.session_state.rap, st.session_state.save, st.session_state.std = engine.calculate_all_plans(
                    balance=balance,
                    grad_loan_balance=grad_loan_balance,
                    interest=interest,
                    agi=agi,
                    household_size=household_size,
                    num_of_dependents=num_of_dependents,
                    state=state,
                    borrower_type=borrower_type
                )


def configure_plan_selection_menu() -> None:
    st.selectbox("**⬇️ Select a Payment Plan for Comparison**:",
                 options=[
                     "Saving on a Valuable Education (SAVE)", "Revised Pay As You Earn (REPAYE)",
                     "Pay As You Earn (PAYE)", "Repayment Assistance Plan (RAP)",
                     "Income-Based Repayment (IBR)", "Income-Contingent Repayment (ICR)",
                     "Traditional Repayment Plan"],
                 index=None, placeholder="Choose a Repayment Plan", key="comparison_plan")


# Display comparison between Loan Servicer Estimate and Repayment Plan Estimate
def display_plan_comparison() -> None:
    plans = {
        "Income-Based Repayment (IBR)": st.session_state.ibr,
        "Income-Contingent Repayment (ICR)": st.session_state.icr,
        "Pay As You Earn (PAYE)": st.session_state.paye,
        "Revised Pay As You Earn (REPAYE)": st.session_state.repaye,
        "Repayment Assistance Plan (RAP)": st.session_state.rap,
        "Saving on a Valuable Education (SAVE)": st.session_state.save,
        "Traditional Repayment Plan": st.session_state.std
    }

    col1, col2 = st.columns(2)
    with col1:
        # Uses a default value to prevent "None" from showing up on cards
        if st.session_state.servicer_estimate is None:
            servicer_est = 0
        else:
            servicer_est = st.session_state.servicer_estimate

        st.metric("**Your Loan Servicer's Provided Monthly Payment Estimate**",
                  value=f"{servicer_est}",
                  format="dollar", border=True)

    with col2:
        # Provide a sensible default
        plan = st.session_state.get("comparison_plan", "Traditional Repayment Plan")

        # NOTE: Is this redundant?
        # TODO: Refactor this out if possible
        if plan not in plans:
            plan = "Traditional Repayment Plan"

        selected_plan_est = plans[plan]
        st.metric(f"**Monthly Payment Estimate under {plan}**",
                  value=f"{selected_plan_est}", format="dollar", border=True)

    engine.display_flagged_diff(
        selected_plan_est=selected_plan_est,
        servicer_estimate=servicer_est
    )


@st.dialog("Before you begin!")
def spawn_loan_input_checklist() -> None:
    st.html(
    """
    <style>
        button[aria-label="Close"] {
            background-color: rgb(255, 75, 75) !important;
            color: white !important;

            display: flex !important;
            align-items: center !important;
            justify-content: center !important;

            width: 30px !important;
            height: 30px !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }
    </style>
    """
    )
    st.markdown("Gathering all of your loan details can be a headache, so we've provided a small checklist to make sure you have everything in one place before you begin.")

    st.checkbox("**Student-Loan Servicer** or **FSA** Payment Plan Estimate in USD ($)")
    st.checkbox("**Total Outstanding Loan Amount** in USD ($)")
    st.checkbox("Your Loan's **Annual Interest Rate** as a Percentage (%)")
    st.checkbox("Your **Adjusted Gross Income** in USD ($)", help=st.session_state.get("agi_helper"))
    st.checkbox("Does Your Loan Originate **Before** or **After** July 1st, 2014?")


@st.dialog("Want to get connected?")
def spawn_get_connected_popup() -> None:
    st.html(
    """
    <style>
        button[aria-label="Close"] {
            background-color: rgb(255, 75, 75) !important;
            color: white !important;

            display: flex !important;
            align-items: center !important;
            justify-content: center !important;

            width: 30px !important;
            height: 30px !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }
    </style>
    """
    )
    st.markdown("We at the debt collective understand that this is a sensitive topic, so we protect your information at every step.")
    st.markdown("Click here to see our [data privacy policy](google.com).")

    # Users opt-in to the information they want to share and their desired level of engagement with the Debt Collective.
    st.checkbox("I want to get in contact with Debt Collective Staff (Loan Help?)",
                key="get_connected_to_dc_staff")
    st.checkbox("I want to get involved as a volunteer in the Debt Collective.",
                key="get_connected_as_volunteer")
    st.checkbox("I want to share my data with the Debt Collective (Case Building Data)",
                key="get_connected_to_dc_case")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Email:", placeholder="Enter your email here")

    with col2:
        st.selectbox("State:",
                     options=["Prefer not to say", "AL", "AK", "AZ", "AR", 
                             "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
                             "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                             "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV",
                             "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
                             "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT",
                             "VT", "VA", "WA", "WV", "WI", "WY", "DC", "AS",
                             "GU", "MP", "PR", "VI"],
                    help="Your State or Territory of Residence",
                    index=None
                    )

    # After they're all done selecting from the checkboxes, then they can submit their info.
    # TODO: Implement the actual functionality of this - Likely needs DC backend help
    st.button("Submit")


def configure_share_button() -> None:
    # NOTE: Prevent the button from being pressed too early?
    st.button("Share Results", on_click=spawn_get_connected_popup, type="primary")


@st.dialog(f"How We Calculated Your Estimate: {st.session_state.get("comparison_plan", "Traditional Repayment Plan")}")
def spawn_payment_plan_explainer_popup() -> None:
    st.html(
    """
    <style>
        button[aria-label="Close"] {
            background-color: rgb(255, 75, 75) !important;
            color: white !important;

            display: flex !important;
            align-items: center !important;
            justify-content: center !important;

            width: 30px !important;
            height: 30px !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }
    </style>
    """
    )
    balance = init_sensible_default_for(st.session_state.total_balance, value=0.0)
    grad_loan_balance = init_sensible_default_for(st.session_state.grad_loan_balance, value=0.0)
    total_balance = balance + grad_loan_balance
    interest = init_sensible_default_for(st.session_state.annual_interest_rate, value=0.0)
    agi = init_sensible_default_for(st.session_state.agi, value=0.0)
    household_size = init_sensible_default_for(st.session_state.household_size, value=0)
    num_of_dependents = init_sensible_default_for(st.session_state.num_of_dependents, value=0)
    state = st.session_state.get("state_of_residency", "contiguous")
    borrower_type = "new" if "new" in str(st.session_state.borrower_type).lower() else "old"

    # TODO: Extract this from spawn_payment_plan_explainer_popup()
    def msg_contains(param_names: list[str] | None = None):
        msg = f""
        loan_inputs = {"balance": f"""Your undergraduate loan balance is \${balance:,.2f}
        \n""",
        "total_balance": f"""Your outstanding balance is \${total_balance:,.2f}
        \n""",
        "grad_loan_balance": f"""your grad loan balance is \${grad_loan_balance:,.2f}
        \n""",
        "interest": f"""Your interest rate is {interest:,.2f}%
        \n""",
        "state": f"""You live in {"the **" + state if state != "alaska" or state != "hawaii" else state}**.
        \n""",
        "agi": f"""Your AGI is \${agi:,.2f}
        \n""",
        "household_size": f"""Your household size is {household_size:d}
        \n""",
        "num_of_dependents": f"""Your number of dependents is {num_of_dependents:d}
        \n""",
        "borrower_type": f"""Your loan originates **{"before July 1st, 2014"
                                if borrower_type == "old"
                                else "after July 1st, 2014"}**.
        \n""",
        "years": "Assuming a repayment period of **15 years**."}

        if not param_names:
            msg = "".join([loan_inputs[fragment] for fragment in loan_inputs])
            return msg

        for param in param_names:
            if param in loan_inputs:
                msg += loan_inputs[param]
        return msg

    plan_explanations = {
        "Income-Based Repayment (IBR)": msg_contains(["balance", "interest", "agi", "household_size", "state", "borrower_type"]),
        "Income-Contingent Repayment (ICR)": msg_contains(["balance", "interest", "agi", "household_size", "state"]),
        "Pay As You Earn (PAYE)": msg_contains(["balance", "interest", "agi", "household_size", "state"]),
        "Revised Pay As You Earn (REPAYE)": msg_contains(["balance", "interest", "agi", "household_size", "state", "borrower_type"]),
        "Repayment Assistance Plan (RAP)": msg_contains(["agi", "num_of_dependents"]),
        "Saving on a Valuable Education (SAVE)": msg_contains(["balance", "grad_loan_balance", "agi", "household_size", "state"]),
        "Traditional Repayment Plan": msg_contains(["balance", "interest", "years"])
    }

    if st.session_state["comparison_plan"] in plan_explanations:
        key = st.session_state.get("comparison_plan", "Traditional Repayment Plan")
        explainer = plan_explanations.get(key, "Traditional Repayment Plan")
        st.markdown(explainer)



def configure_calculation_explainer_button() -> None:
    st.button("How Did We Get This?", on_click=spawn_payment_plan_explainer_popup, type="primary")


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

    col1, col2 = st.columns([0.75, 0.15])
    with col1:
        configure_share_button()
    with col2:
        configure_calculation_explainer_button()
    configure_footer()

    # Pop up comes up after all page contents have loaded
    # Wait for a couple seconds if it hasn't been called already
    time.sleep(5.0)
    if not st.session_state.input_checklist_timer_done:
        st.session_state.input_checklist_timer_done = True
        spawn_loan_input_checklist()


if __name__=="__main__":
    main()