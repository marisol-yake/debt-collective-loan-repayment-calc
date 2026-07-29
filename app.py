# Defines application UI layout and content
# ref: https://www.youtube.com/watch?v=c8QXUrvSSyg
import streamlit as st
import engine
import time


def init_session_state() -> None:
    defaults = {
        "ibr": 0.0,
        "icr": 0.0,
        "paye": 0.0,
        "repaye": 0.0,
        "rap": 0.0,
        "std": 0.0,

    "input_checklist_timer_done": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def configure_page() -> None:
    st.html(
        """
        <style>
        [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapseButton"] {
                # height: 3rem;
                # width : 3rem;
                # background-color: RED;
                animation: bounce 2s ease infinite;
                background: #E9ECEF;
                visibility: visible;
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
        # Using a streamlit form prevents calculations from happening automatically
        # This prevents unnecessary computations and makes intended-use clearer
        with st.form(key="input_form"):
            # Accepts all user inputs for loan repayment calculations
            # Setting value=None means that st.number_input is already cleared for users automatically. 
            st.number_input("Servicer Monthly Payment Estimate ($):",
                            min_value=0.0, value=None, step=1.0, placeholder="0.00",
                            help="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                            key="servicer_estimate")
            st.number_input("Total Loan Balance ($):",
                            min_value=0.0, value=None, step=1.0, placeholder="0.00",
                            help="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                            key="total_balance")
            st.number_input("Annual Interest Rate (%):",
                            min_value=0.0, value=None, step=1.0, placeholder="0.00%",
                            help="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                            key="annual_interest_rate")
            st.number_input("Adjusted Gross Income (AGI) ($):",
                            min_value=0.0, value=None, step=1.0, placeholder="0.00",
                            help="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                            key="agi")
            st.number_input("Household Size (For IBR, PAYE, and ICR):",
                            min_value=0, value=None, step=1, placeholder="0",
                            help="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                            key="household_size")
            st.number_input("Number of Dependents (Claimed on taxes - Only For RAP):",
                            min_value=0, value=None, step=1, placeholder="0",
                            key="num_of_dependents")
            st.selectbox("State of Residency:",
                         options=["Contiguous U.S.", "Alaska", "Hawaii"],
                         help="If you don't live in **Alaska** or **Hawaii**, you can use **Contiguous U.S.**",
                         key="state_of_residency")
            st.selectbox("Borrower Type (for IBR):",
                         options=["New Borrower (After July 1, 2014)", "Old Borrower (Before July 1, 2014)"],
                         help="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
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
                st.session_state.ibr, st.session_state.icr, st.session_state.paye, st.session_state.repaye, st.session_state.rap, st.session_state.std = engine.calculate_all_plans(
                    balance=balance,
                    interest=interest,
                    agi=agi,
                    household_size=household_size,
                    num_of_dependents=num_of_dependents,
                    state=state,
                    borrower_type=borrower_type
                )


def configure_plan_selection_menu() -> None:
    st.selectbox("**⬇️ Select a Payment Plan for Comparison**:",
                 options=["Traditional Repayment Plan", "Income-Based Repayment (IBR)",
                 "Income-Contingent Repayment (ICR)", "Pay As You Earn (PAYE)",
                 "Revised Pay As You Earn (REPAYE)", "Repayment Assistance Plan (RAP)"],
                 index=None, placeholder="Choose a Repayment Plan", key="comparison_plan")


# Display comparison between Loan Servicer Estimate and Repayment Plan Estimate
def display_plan_comparison() -> None:
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
    st.markdown("Gathering all of your loan details can be a headache, so we've provided a small checklist to make sure you have everything in one place before you begin.")

    st.checkbox("**Student-Loan Servicer** or **FSA** Payment Plan Estimate in USD ($).")
    st.checkbox("**Total Outstanding Loan Amount** in USD ($).")
    st.checkbox("Your Loan's **Annual Interest Rate** as a Percentage (%)")
    st.checkbox("Your **Adjusted Gross Income** in USD ($).")
    st.checkbox("Does Your Loan Originate **Before** or **After** July 1st, 2014?")

    # TODO: Decide which is less tedious / more intuitive
    # Option 1
    # Streamlit won't let you ignore the dialog modal without just pressing the "X" button
    # Or re-running the app entirely.
    if st.button("I'm ready!", type="primary"):
        st.rerun()

    # Option 2
    st.markdown("Press the '**x**' in the top-right corner of this box to continue.")

@st.dialog("Want to get connected?")
def spawn_get_connected_popup() -> None:
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
    configure_share_button()
    configure_footer()

    # Pop up comes up after all page contents have loaded
    # Wait for a couple seconds if it hasn't been called already
    time.sleep(5.0)
    if not st.session_state.input_checklist_timer_done:
        st.session_state.input_checklist_timer_done = True
        spawn_loan_input_checklist()


if __name__=="__main__":
    main()