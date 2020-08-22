import streamlit as st
import numpy as np
import pandas as pd
from client import AlphaVantageClient
import sys
import plotly.express as px


sys.setrecursionlimit(1500)

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
    "MarketCapitalization",
]

USELESS_ELEMENTS = ["Symbol", "AssetType", "Description", "Name", "FiscalYearEnd", "LatestQuarter"]


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


@st.cache
def load_cash_flow(symbol):
    return client.cash_flow(symbol)


@st.cache
def load_quotes(symbol):
    return client.time_series_daily(symbol)


class StockInfo:
    def __init__(self, symbol):
        self.symbol = symbol

    def company_overview(self):
        data = load_company_info(self.symbol)
        st.subheader(f'{data.get("Name")} Overview')
        st.write(data.get("Description"))
        table_dict = {k: v for k, v in data.items() if k in COMPANY_BASIC_INFORMATION}

        for k, v in table_dict.items():
            st.write(f"* {k}: {v}")

    def balance_sheet_view(self):
        data = load_balance_sheet(self.symbol).get("annualReports")
        data = pd.json_normalize(data).T
        st.subheader("*Balance Sheet*")
        st.write(data)
        data = data.dropna()
        categories = data.index.to_list()
        categories.remove("fiscalDateEnding")
        chart = st.checkbox("Analyze Balance Sheet on Chart")

        if chart:
            chosen_category = st.selectbox("What category, do you want to analyze ? ", categories)
            if chosen_category:
                category_df = data.loc[chosen_category].values
                year = data.loc["fiscalDateEnding"].values
                chart = px.bar(x=year,y=category_df, text=category_df, color=year)
                chart.update_traces(texttemplate='%{text:.2s}', textposition='outside')

                chart.update_layout(legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ))
                st.plotly_chart(figure_or_data=chart)


    def income_statement_view(self):
        data = load_income_statement(self.symbol).get("annualReports")
        data = pd.json_normalize(data).T
        st.subheader("*Income Statement*")
        st.write(data)

    def cash_flow_view(self):
        data = load_cash_flow(self.symbol).get("annualReports")
        data = pd.json_normalize(data).T
        st.subheader("*Cash Flow*")
        st.write(data)

    def quotes_view(self):
        data = load_quotes(self.symbol).get("Time Series (Daily)")
        data = pd.DataFrame(data).T
        st.subheader("*Daily Quotes*")
        st.write(data)

    def kpi_view(self):
        data = load_company_info(self.symbol)
        st.subheader(f'{data.get("Name")}')
        st.write(f'{data.get("Description")}')
        table_dict = {k: v for k, v in data.items() if k not in COMPANY_BASIC_INFORMATION + USELESS_ELEMENTS}
        df = pd.DataFrame(table_dict.items())
        df.columns = ["Label", "Value"]
        st.dataframe(df)


def user_search_input(keyword):
    company = look_for_company(keyword)
    company = pd.DataFrame(company)
    st.table(company)


def home():
    st.markdown(
        f"""

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
    st.title("Stock Analyzer")
    st.empty()
    ticker = st.sidebar.text_input("Enter company ticker (e.g Facebook: FB)")

    if ticker:
        st.sidebar.text(f"{ticker.upper()} was provided\nNow you can switch between pages!")

    stock_element = st.sidebar.selectbox(
        "Choose a page",
        [
            "Home",
            "Company Overview",
            "Balance Sheet",
            "Income Statement",
            "Cash Flow",
            "Stock Quotes",
            "KPI"
        ],
    )

    if stock_element == "Home":
        home()

    if ticker:
        stock = StockInfo(ticker)
        if stock_element == "Company Overview":
            stock.company_overview()
        elif stock_element == "Balance Sheet":
            stock.balance_sheet_view()
        elif stock_element == "Income Statement":
            stock.income_statement_view()
        elif stock_element == "Cash Flow":
            stock.cash_flow_view()
        elif stock_element == "Stock Quotes":
            stock.quotes_view()
        elif stock_element == "KPI":
            stock.kpi_view()

    if stock_element != "Home" and not ticker:
        st.write("You didn't enter correct ticker in the search box on left")


app()
