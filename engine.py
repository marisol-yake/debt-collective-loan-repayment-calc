# Defines underlying application logic
import streamlit as st
import bs4
import js2py
import requests

# Func: Fetch edcaps calculator (JS directly embedded in HTML)
# Use streamlit cache to only refresh the HTML calculator form once per week

# Func: Extract HTML Form - Repayment Calculator

# Func: Extract JS logic

# Func: Streamlit User Inputs (defined by edcaps form params)
#           -> ([IDR Plans], Traditional Payment Plan) monthly payment amounts

# Func: Create popup if there is a flagged difference
# TODO: Make sure it pops-up only once per session (How?)