# A one-to-one translation of the EDCAP calculator
# ref: https://www.edcapny.org/wp-content/uploads/2026/07/Repayment-Plan-Calculator-7.6.26.html
import math
from typing import Any, Union
import streamlit as st


type USD = Union[int, float]
type InterestRate = float
type BorrowerType = str
type Factor = float
type ChartEntry = dict[str, Union[USD, Factor]]
type Chart = list[ChartEntry]
type PovertyGuideline = int
type USDPaymentAmount = USD
type PaymentPlanDetails = dict[str, Any]


###########################################################################
# Custom Application Logic
###########################################################################
def _format_flagged_diff_display_value(difference: USD, percent_difference: float):
    # If the percent difference is greater than or equal to 20% in either direction
    # Mark red, known as a "flagged difference"
    # Nicely formated as +-$
    # This: +$200 and -$200
    # Instead of: $200 and $-200
    display_value = f"${abs(difference):0,.2f} ({percent_difference:0,.0%})"

    if abs(percent_difference) >= 0.2:
        st.html("""
                <style>
                    /* Color flagged differences as red */
                    .st-key-metric-card [data-testid="stMetricValue"] {
                        color: #dc3545 !important;
                    }
                </style>
                """)
        if percent_difference > 0:
            display_value = display_value.replace("$", "+$").replace("(", "(+")
        else:
            display_value = display_value.replace("$", "-$")

    return display_value


def display_flagged_diff(*, selected_plan_est: USD, servicer_estimate: USD) -> None:
    difference = servicer_estimate - selected_plan_est

    # Handles edge cases where comparison is 0 / 0
    if selected_plan_est == 0:
        # Case 1: Where selected plan payment amount = 0 and servicer estimate = 0
        if servicer_estimate == 0:
            percent_diff = 0.0
        # Case 2: Where selected plan payment amount = 0 and servicer estimate != 0
        else:
            percent_diff = 1.0  
    else:
        # Case 3: Both estimates are not equal to 0
        percent_diff = difference / selected_plan_est

    with st.container(key="metric-card"):
        display_value = _format_flagged_diff_display_value(
            difference=difference,
            percent_difference=percent_diff
        )
        st.metric("**Total Difference**", value=display_value, border=True)


###########################################################################
# 1-to-1 EDCAP Calculator Logic Translation (Javascript -> Python)
###########################################################################
poverty_guidelines = {
    "contiguous": [15960, 21640, 27320, 33000, 38680, 44360, 50040, 55720],
    "alaska": [19950, 27050, 34150, 41250, 48350, 55450, 62550, 69650],
    "hawaii": [18360, 24890, 31420, 37950, 44480, 51010, 57540, 64070]
}

extra_person = {
    "contiguous": 5680,
    "alaska": 7100,
    "hawaii": 6530
}


def _get_poverty_guideline(state: str, household_size: int) -> PovertyGuideline:
    table = poverty_guidelines[state]

    if household_size <= 8:
        result = table[household_size - 1]
    else:
        result = table[7] + extra_person[state] * (household_size - 8)

    return result


def calculate_standard_payment(balance: USD, interest: InterestRate, years: int = 10) -> USDPaymentAmount:
    r = (interest / 100) / 12
    n = years * 12

    if r == 0:
        result = balance / n
    else:
        result = balance * r * math.pow(1 + r, n) / (math.pow(1 + r, n) - 1)

    return result


def _calculate_fixed_payment(balance: USD, interest: InterestRate, years: int = 12) -> USDPaymentAmount:
    r = (interest / 100) / 12
    n = years * 12
    
    if r == 0:
        result = balance / n
    else:
        result = balance * r * math.pow(1 + r, n) / (math.pow(1 + r, n) - 1)

    return result


chart1 = [
    { "agi": 13717, "factor": 55.00 }, { "agi": 18873, "factor": 57.79 },
    { "agi": 24285, "factor": 60.57 }, { "agi": 29819, "factor": 66.23 },
    { "agi": 35104, "factor": 71.89 }, { "agi": 41769, "factor": 80.33 },
    { "agi": 52462, "factor": 88.77 }, { "agi": 65798, "factor": 100.00 },
    { "agi": 79138, "factor": 100.00 }, { "agi": 95112, "factor": 111.80 },
    { "agi": 121787, "factor": 123.50 }, { "agi": 172492, "factor": 141.20 },
    { "agi": 19779, "factor": 150.00 }, { "agi": 352277, "factor": 200.00 }
]

chart2 = [
    { "agi": 13717, "factor": 50.52 }, { "agi": 21641, "factor": 56.68 },
    { "agi": 25790, "factor": 59.56 }, { "agi": 33717, "factor": 67.79 },
    { "agi": 41769, "factor": 75.22 }, { "agi": 52462, "factor": 87.61 },
    { "agi": 65797, "factor": 100.00 }, { "agi": 79138, "factor": 100.00 },
    { "agi": 99146, "factor": 109.40 }, { "agi": 132481, "factor": 125.00 },
    { "agi": 179158, "factor": 140.60 }, { "agi": 250560, "factor": 150.00 },
    { "agi": 409433, "factor": 200.00 }
]


def _get_chart_ICR(household_size: int) -> Chart:
    if household_size == 1:
        result = chart1
    else:
        result = chart2

    return result


def _find_surrounding_AGIs(chart: Chart, agi: USD) -> tuple[ChartEntry, ChartEntry]:
    lower, higher = chart[0], chart[-1]

    for idx, entry in enumerate(chart):
        if agi >= chart[idx]["agi"] and agi < chart[idx + 1]["agi"]:
            lower = chart[idx]
            higher = chart[idx + 1]
            break

    return lower, higher


def calculate_ICR(balance: USD, interest: InterestRate, agi: USD, household_size: int, state: str) -> PaymentPlanDetails:
    poverty_level = _get_poverty_guideline(state, household_size)
    discretionary_income = max(agi - poverty_level, 0)
    monthly_discretionary = discretionary_income / 12
    discretionary_payment = monthly_discretionary * 0.20

    base_payment = _calculate_fixed_payment(balance, interest)
    chart = _get_chart_ICR(household_size)

    if (household_size == 1 and agi >= 352418) or (household_size > 1 and agi >= 409597):
        ipf = 200.0
    else:
        lower, higher = _find_surrounding_AGIs(chart, agi)

        if lower["agi"] == higher["agi"]:
            ipf = lower["factor"]
        else:
            ratio = (agi - lower["agi"]) / (higher["agi"] - lower["agi"])
            ipf = lower["factor"] + ratio * (higher["factor"] - lower["factor"])

    income_adjusted_payment = (ipf / 100) * base_payment
    icr_payment = min(discretionary_payment, income_adjusted_payment)

    return {
        "plan": "Income-Contingent Repayment (ICR)",
        "monthly_payment": icr_payment,
        "discretionary_percent": 20,
        "forgiveness_years": 25,
        "notes": "Lower of 20% of discretionary income or 12-year fixed payment adjusted for income."
    }


def calculate_IBR(balance: USD, interest: InterestRate, agi: USD, household_size: int, state: str, borrower_type: BorrowerType) -> PaymentPlanDetails:
    poverty = _get_poverty_guideline(state, household_size)
    poverty150 = poverty * 1.5
    discretionary_income = max((agi - poverty150), 0)
    percent = 0.10 if borrower_type == "new" else 0.15
    forgiveness_years = 20 if "new" else 25

    annual_payment = discretionary_income * percent
    monthly_payment = annual_payment / 12
    standard_monthly = calculate_standard_payment(balance, interest)
    
    if (monthly_payment > standard_monthly):
        monthly_payment = standard_monthly

    return {
        "plan": "Income-Based Repayment (IBR)",
        "monthly_payment": monthly_payment,
        "percent": percent * 100,
        "forgiveness_years": forgiveness_years,
        "notes": "Capped at 10-year standard plan."
    }


def calculate_PAYE(balance: USD, interest: InterestRate, agi: USD, household_size: int, state: str) -> PaymentPlanDetails:
    poverty = _get_poverty_guideline(state, household_size);
    poverty150 = poverty * 1.5;
    discretionary_income = max(agi - poverty150, 0);
    percent = 0.10;
    forgiveness_years = 20;

    annual_payment = discretionary_income * percent;
    monthly_payment = annual_payment / 12;
    standard_monthly = calculate_standard_payment(balance, interest);
    
    if (monthly_payment > standard_monthly):
        monthly_payment = standard_monthly

    return {
        "plan": "Pay As You Earn (PAYE)",
        "monthly_payment": monthly_payment,
        "percent": percent * 100,
        "forgiveness_years": forgiveness_years,
        "notes": "Capped at 10-year standard plan."
    }


def calculate_REPAYE(balance: USD, interest: InterestRate, agi: USD, household_size: int, state: str, borrower_type: BorrowerType) -> USD:
    ibr_payments = calculate_IBR(balance, interest, agi, household_size, state, borrower_type)["monthly_payment"]
    return ibr_payments * 0.666


def _get_RAP_percentage(agi: USD) -> float:
    if (agi <= 10000): return 0
    if (agi <= 20000): return 0.01
    if (agi <= 30000): return 0.02
    if (agi <= 40000): return 0.03
    if (agi <= 50000): return 0.04
    if (agi <= 60000): return 0.05
    if (agi <= 70000): return 0.06
    if (agi <= 80000): return 0.07
    if (agi <= 90000): return 0.08
    if (agi <= 100000): return 0.09
    return 0.10


def calculate_RAP(agi: USD, num_of_dependents: int) -> PaymentPlanDetails:
    percentage = _get_RAP_percentage(agi)
    monthly_payment = (agi * percentage) / 12 - (50 * num_of_dependents)
    monthly_payment = max(10, monthly_payment)

    return {
        "plan": "Repayment Assistance Plan (RAP)",
        "monthly_payment": monthly_payment,
        "discretionary_percent": (percentage * 100),
        "forgiveness_years": 30,
        "notes": "% of AGI minus $50 per dependent claimed on tax return. Minimum $10/month."
    }


def calculate_all_plans(*, balance: USD, interest: InterestRate, agi: USD, household_size: int, num_of_dependents: int, state: str, borrower_type: BorrowerType):

    # TODO: Implement this
    # if not balance or not interest or not agi or not household_size or num_of_dependents is None:
    #     # MissingCalculatorParameters
    #     # alert("Please fill in all fields with valid values.")
    #     return

    # TODO: Implement this
    # if not borrower_type:
    #     # MissingBorrowerType
    #     # alert("Please select a borrower type for IBR calculation.");
    #     return

    ibr = calculate_IBR(balance, interest, agi, household_size, state, borrower_type)["monthly_payment"]
    icr = calculate_ICR(balance, interest, agi, household_size, state)["monthly_payment"]
    paye = calculate_PAYE(balance, interest, agi, household_size, state)["monthly_payment"]
    repaye = calculate_REPAYE(balance, interest, agi, household_size, state, borrower_type)
    rap = calculate_RAP(agi, num_of_dependents)["monthly_payment"]
    std = calculate_standard_payment(balance, interest, years=15)

    # NOTE: These don't end up in the relevant calculator results
    # NOTE: but I'm keeping them just in case
    # def _getPaybackPeriod(balance):
    #     if (balance < 25000): return 10
    #     if (balance < 50000): return 15
    #     if (balance < 100000): return 20
    #     return 25

    # payback_years = _getPaybackPeriod(balance)
    # standard_monthly_payment = _calculate_fixed_payment(balance, interest, payback_years)
    # total_paid = standard_monthly_payment * 12 * payback_years
    # starting_interest = (balance * (interest / 100)) / 12

    return ibr, icr, paye, repaye, rap, std
