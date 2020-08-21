import streamlit as st
import numpy as np
import pandas as pd
from client import AlphaVantageClient


client = AlphaVantageClient()


COMPANY_BASIC_INFORMATION = [
    "Exchange",
    "Currency",
    "Country",
    "Sector",
    "Technology",
    "Industry",
    "Address",
    "FullTimeEmployees",
    "MarketCapitalization"
]

not_needed_elements = ['Symbol','AssetType','Description',"Name","FiscalYearEnd"]


@st.cache
def load_company_info(symbol):
    return client.company_overview(symbol)


@st.cache
def load_balance_sheet(symbol):
    return client.balance_sheet(symbol)


@st.cache
def look_for_company(keyword):
    return client.search(keyword).get("bestMatches")


@st.cache
def load_income_statement(symbol):
    return client.income_statement(symbol)


def company_overview(ticker):
    data = load_company_info(ticker)
    st.subheader(f'{data.get("Name")} Overview')
    st.write(data.get("Description"))
    table_dict = {k: v for k, v in data.items() if k in COMPANY_BASIC_INFORMATION}

    for k, v in table_dict.items():
        st.write(f"* {k}: {v}")


def balance_sheet_view(ticker):
    data = load_balance_sheet(ticker).get("annualReports")
    data = pd.json_normalize(data).T
    data.columns = data.iloc[0]
    st.write(data)


def income_statement_view(ticker):
    data = load_income_statement(ticker).get("annualReports")
    data = pd.json_normalize(data).T
    data.columns = data.iloc[0]
    st.write(data)


def cash_flow_view(ticker):
    data = cash_flow_view(ticker).get("annualReports")
    data = pd.json_normalize(data).T
    data.columns = data.iloc[0]
    st.write(data)


def user_search_input(input):
    company = look_for_company(input)
    company = pd.DataFrame(company)
    st.table(company)


def home():
    st.markdown(
        f"""
            ### Nutshell

            Application uses AlphaVantage API to fetch financial data like 
            financial statements, company basic info, KPI's and Quotes.

            On the Left side you have a panel where you can provide stock's
            ticker and choose the page that you want to look at. You can analyze 
            * Income Statement 
            * Balance Sheet  
            * Cash Flow  
            * Quotes  
            * Company Overview  

            If you want to search for a company ticker you can use search box below. 
            If you find company that you are interested at, just provide the ticker
            on the panel at left side of screen and press enter. 
            Now you can analyze all of the elements of report. 

        """
    )
    user_input = st.text_input("Enter company keywords that you are looking for")
    if user_input:
        user_search_input(user_input)

def app():
    st.title('Stock Analyzer')

    ticker = st.sidebar.text_input(
        "Enter company ticker (e.g Facebook: FB)", #value="FB"
    )

    stock_element = st.sidebar.selectbox(
        "Choose a page", ["Home", "Company Overview", "Balance Sheet", "Income Statement", "Cash Flow", "Stock Quotes"]
    )

    if stock_element == "Home":
        home()
    if stock_element == "Company Overview":
        company_overview(ticker)
    elif stock_element == "Balance Sheet":
        balance_sheet_view(ticker)
    elif stock_element == "Income Statement":
        income_statement_view(ticker)
    elif stock_element == "Cash Flow":
        cash_flow_view(ticker)
    elif stock_element == "Stock Quotes":
        pass
    else:
        pass


app()