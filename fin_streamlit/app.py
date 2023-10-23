import streamlit as st

from fin_streamlit.mvc import DashboardController


PAGES = [
    "Home",
    "Company Overview",
    "Balance Sheet",
    "Income Statement",
    "Cash Flow",
    "Stock Quotes",
    "KPI",
]

D = {"Home": DashboardController.load_home_page}


def _dispatcher(page: str, controller: DashboardController):
    pass


def app():
    st.title("Stock Analyzer")
    st.empty()
    symbol = st.sidebar.text_input("Enter company ticker (default: AMZN)", value="AMZN")

    stock_element = st.sidebar.selectbox("Choose page", PAGES)
    if symbol:
        st.sidebar.text(
            f"{symbol.upper()} was provided\nNow you can switch between pages!"
        )
        controller = DashboardController(symbol)

        if stock_element == "Home":
            controller.load_home_page()

        elif stock_element == "Company Overview":
            controller.load_company_info()

        elif stock_element == "Balance Sheet":
            controller.load_balance_sheet()

        elif stock_element == "Income Statement":
            controller.load_income_statement()

        elif stock_element == "Cash Flow":
            controller.load_cashflow()

        elif stock_element == "Stock Quotes":
            controller.load_quotes()

        elif stock_element == "KPI":
            controller.load_kpis()

    if stock_element != "Home" and not symbol:
        st.write("You didn't enter correct symbol in the search box on left")


app()
