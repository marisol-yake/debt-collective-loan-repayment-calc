# A one-to-one translation of the EDCAP calculator
# ref: https://www.edcapny.org/wp-content/uploads/2026/07/Repayment-Plan-Calculator-7.6.26.html
import math
from typing import Any, Union
import streamlit as st

type Number = Union[int, float]
type USD = Number
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
def calculate_difference(a: Number, b: Number) -> tuple[Number, Number]:
    difference = a - b

    # Handles edge cases where comparison is 0 / 0
    if b == 0:
        # Case 1: Where selected plan payment amount = 0 and servicer estimate = 0
        if a == 0:
            percent_difference = 0.0
        # Case 2: Where selected plan payment amount = 0 and servicer estimate != 0
        else:
            percent_difference = 1.0
    else:
        # Case 3: Both estimates are not equal to 0
        percent_difference = difference / b

    return difference, percent_difference


def _format_flagged_diff_display_value(difference: USD, percent_difference: float) -> str:
    # If the percent difference is greater than or equal to 20% in either direction
    # Mark red, known as a "flagged difference"
    # Nicely formated as +-$
    # This: +$200 and -$200
    # Instead of: $200 and $-200
    display_value = f"${abs(difference):0,.2f} ({percent_difference:0,.0%})"

    # If the percent difference is greater than 20%, then mark as flagged difference (e.g. color red)
    if abs(percent_difference) >= 0.2:
        st.html("""
                <style>
                    /* Color flagged differences as red */
                    .st-key-metric-card [data-testid="stMetricValue"] {
                        color: #dc3545 !important;
                    }
                </style>
                """)

        if percent_difference >= 0.2:
            display_value = display_value.replace("$", "+$").replace("(", "(+")
        elif percent_difference <= -0.2:
            display_value = display_value.replace("$", "-$")

    return display_value


def display_flagged_diff(*, selected_plan_est: USD, servicer_estimate: USD) -> None:
    if selected_plan_est is None:
        selected_plan_est = 0
    elif servicer_estimate is None:
        servicer_estimate = 0

    difference, percent_diff = calculate_difference(servicer_estimate, selected_plan_est)

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

    # Edge Case 1: If AGI is less than or equal to the lowest entry
    if agi <= chart[0]["agi"]:
        return chart[0], chart[0]

    # Edge Case 2: If AGI exceeds or equals the highest entry (e.g., $5,000,000)
    if agi >= chart[-1]["agi"]:
        # Return the highest entry for both boundaries
        return chart[-1], chart[-1]

    for current_entry, next_entry in zip(chart, chart[1:]):
        if current_entry["agi"] <= agi < next_entry["agi"]:
            return current_entry, next_entry

    return lower, higher


def calculate_ICR(balance: USD, interest: InterestRate, agi: USD, household_size: int, state: str) -> PaymentPlanDetails:
    """
    **Monthly Payment**:
    - Your monthly payment will be the lesser of
        - 20 percent of discretionary income, or
        - the amount you would pay on a repayment plan with a fixed payment over 12 years, adjusted according to your income.
    - Payments are recalculated each year and are based on your updated income, family size, and the total amount of your Direct Loans.
    - You must update your income and family size each year, even if they haven’t changed.
    - If you’re married, your spouse’s income or loan debt will be considered only if you file a joint tax return or you choose to repay your Direct Loans jointly with your spouse.

    **Time Frame**:
    - Any outstanding balance will be forgiven if you haven’t repaid your loan in full after 25 years.
    - You may have to pay income tax on any amount that is forgiven.

    **Eligible Loans**:
    - Direct Subsidized and Unsubsidized Loans
    - Direct PLUS Loans made to students
    - Direct Consolidation Loans

    ref: https://edfinancial.studentaid.gov/income-driven-repaymentinformation-center/icr
    """
    poverty_level = _get_poverty_guideline(state, household_size)
    discretionary_income = max(agi - poverty_level, 0)
    monthly_discretionary = discretionary_income / 12
    discretionary_payment = monthly_discretionary * 0.20

    base_payment = _calculate_fixed_payment(balance, interest, years=12)
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
    """
    **Monthly Payment**:
    - Your monthly payments will be either 10 or 15 percent of discretionary income (depending on when you received your first loans), but never more than you would have paid under the 10-year Standard Repayment Plan.
    - Payments are recalculated each year and are based on your updated income and family size.
    - You must update your income and family size each year, even if they haven’t changed.
    - If you’re married, your spouse’s income or loan debt will be considered only if you file a joint tax return.

    **Time Frame**:
    - Any outstanding balance on your loan will be forgiven if you haven’t repaid your loan in full after 20 or 25 years, depending on when you received your first loans.
    - You may have to pay income tax on any amount that is forgiven. 

    **Eligible Loans**:
    - Direct Subsidized and Unsubsidized Loans
    - Subsidized and Unsubsidized Federal Stafford Loans
    - all PLUS Loans made to students
    - Consolidation Loans (Direct or FFEL) that do not include PLUS loans (Direct or FFEL) made to parents

    ref: https://edfinancial.studentaid.gov/income-driven-repaymentinformation-center/ibr1
    """
    poverty = _get_poverty_guideline(state, household_size)
    poverty150 = poverty * 1.5
    discretionary_income = max((agi - poverty150), 0)
    percent = 0.10 if borrower_type == "new" else 0.15
    forgiveness_years = 20 if borrower_type == "new" else 25

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
    """
    **Monthly Payment**:
    - Discretionary Income = Your Income – (150% × HHS federal poverty guidelines)
    - Reduced by $50 for each dependent on your federal tax return
    - Total monthly payment may not be less than $10

    **Time Frame**:
    - First available to borrowers in 2012, PAYE is a federal income-driven repayment plan available to certain U.S. student loan borrowers.
    - Payments are based on your income and are made for a maximum of 240 monthly payments (20 years). Any amounts remaining after 240 monthly payments are forgiven.

    **Eligible Loans**:
    - You must be a new borrower as of October 1, 2007, and must have received at least one Federal Direct Loan disbursed after October 1, 2011. You are a new borrower if you have never received a loan prior to October 1, 2007, or you have paid in full any federal loan balances received prior to receiving a new loan after October 1, 2007.
    - Only Federal Direct loans qualify for PAYE. Other federal loan types (Federal Family Education Loans, Federal Perkins, and Health Professions Student Loans) disbursed after October 1, 2007, are eligible if consolidated into a Direct Consolidation loan.
    - If the payments due under PAYE are less than the payments that would be due under a standard 10-year repayment plan, you have a partial financial hardship (PFH). A rule of thumb: If your debt exceeds your income, you likely demonstrate a PFH under PAYE.

    ref: https://www.vin.com/studentdebtcenter/default.aspx?pid=14352&catId=74141&id=7250325
    """
    poverty = _get_poverty_guideline(state, household_size)
    poverty150 = poverty * 1.5
    discretionary_income = max(agi - poverty150, 0)
    percent = 0.10
    forgiveness_years = 20

    annual_payment = discretionary_income * percent
    monthly_payment = annual_payment / 12
    standard_monthly = calculate_standard_payment(balance, interest)
    
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
    """
    **Monthly Payment**:
    - The REPAYE Plan helps keep a borrower’s monthly student loan payments affordable by capping the payment amount at 10% of the borrower’s discretionary income.
    - ... all Direct loan student borrowers [are granted] the ability to cap their monthly payments at 10% of their “discretionary income,” defined as **adjusted gross income** above **150%** of the applicable **poverty guideline** divided by twelve.

    **Time Frame**:
    - Borrowers in REPAYE whose only eligible Direct loan debt is for undergraduate education will have any outstanding balance forgiven after 20 years of repayment.
    - Borrowers with eligible Direct loan debt received for any graduate or professional education will have their balance forgiven after 25 years.

    **Eligible Loans**:
    - All Direct Loan borrowers

    ref: https://studentloanborrowerassistance.org/the-revised-pay-as-you-earn-repaye-plan-is-now-available/
    ref: https://fsapartners.ed.gov/fsa-print/publication/8658
    """
    poverty = _get_poverty_guideline(state, household_size)
    poverty150 = poverty * 1.5
    discretionary_income = max((agi - poverty150), 0)
    forgiveness_years = 20 if borrower_type == "new" else 25
    percent = 0.10

    annual_payment = discretionary_income * percent
    monthly_payment = annual_payment / 12
    standard_monthly = calculate_standard_payment(balance, interest)
    
    if (monthly_payment > standard_monthly):
        monthly_payment = standard_monthly

    # NOTE: Previous calculation
    # ibr_payments = calculate_IBR(balance, interest, agi, household_size, state, borrower_type)["monthly_payment"]
    # return ibr_payments * 0.666

    return monthly_payment


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
    """
    **Monthly Payment**:
    - A percentage of your adjusted gross income (AGI) up to 10%, divided by 12
    - Reduced by $50 for each dependent on your federal tax return
    - Total monthly payment may not be less than $10

    **Time Frame**:
    - Any outstanding balance will be forgiven if you haven’t repaid your loan in full after 30 years of qualifying payments.
    - Any amount that is forgiven may be considered income for tax purposes.

    **Eligible Loans**:
    - Direct Loans
    - Direct PLUS loans for graduate or professional students
    - Direct Consolidation loans that do not include a Parent PLUS loan

    ref: https://edfinancial.studentaid.gov/income-driven-repaymentinformation-center/rap
    """
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


def calculate_SAVE(agi: USD, household_size: int, state: str, balance: USD, grad_loan_balance: USD = 0):
    """
    **Monthly Payment**:
    - Multiply 2.25 times your poverty level number
    - Subtract the answer from step 1 from your AGI
    - Payments on undergraduate loans will be cut in half (from 10% to 5% of incomes above 225% of FPL).
    - Borrowers who have undergraduate and graduate loans will pay a weighted average of between 5% and 10% of their income based upon the original principal balances of their loans.
    - Multiply the answer from step 2 by 0.1
    - Divide the answer from step 3 by 12

    **Eligible Loans**:
    - Direct Subsidized Loans
    - Direct Unsubsidized Loans,
    - Direct PLUS Loans made to graduate or professional students, and
    - Direct Consolidation Loans that did not repay any PLUS loans made to parents

    ref: https://www.law.uchicago.edu/save-repayment-plan-faq
    ref: https://www.reddit.com/r/StudentLoans/comments/16cgnup/calculate_save_plan_payment_how_to/
    """
    poverty = _get_poverty_guideline(state, household_size)
    poverty225 = poverty * 2.25
    discretionary_income = max((agi - poverty225), 0)
    total_loan_balance = balance + grad_loan_balance
    grad_loan_burden_percent = max(((total_loan_balance - balance) / total_loan_balance), 0) * 0.05
    percent = 0.05 + grad_loan_burden_percent

    annual_payment = discretionary_income * percent
    monthly_payment = annual_payment / 12

    return monthly_payment


def calculate_all_plans(*, balance: USD, grad_loan_balance: USD, interest: InterestRate, agi: USD, household_size: int, num_of_dependents: int, state: str, borrower_type: BorrowerType):
    if grad_loan_balance > 0:
        total_balance = balance + grad_loan_balance
    else:
        total_balance = balance

    ibr = calculate_IBR(total_balance, interest, agi, household_size, state, borrower_type)["monthly_payment"]
    icr = calculate_ICR(total_balance, interest, agi, household_size, state)["monthly_payment"]
    paye = calculate_PAYE(total_balance, interest, agi, household_size, state)["monthly_payment"]
    repaye = calculate_REPAYE(total_balance, interest, agi, household_size, state, borrower_type)
    rap = calculate_RAP(agi, num_of_dependents)["monthly_payment"]
    save = calculate_SAVE(agi, household_size, state, balance, grad_loan_balance)
    std = calculate_standard_payment(total_balance, interest, years=15)

    return ibr, icr, paye, repaye, rap, save, std
