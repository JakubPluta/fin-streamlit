from typing import Any

import streamlit as st

from fin_streamlit.mvc.controller import DashboardController

_PAGES_VIEWS_MAP = {
    "Home": DashboardController.load_home_page,
    "Company Overview": DashboardController.load_company_info,
    "Balance Sheet": DashboardController.load_balance_sheet,
    "Income Statement": DashboardController.load_income_statement,
    "Cash Flow": DashboardController.load_cashflow,
    "Stock Quotes": DashboardController.load_quotes,
    "KPI": DashboardController.load_kpis,
}


def dispatch_view(page: str, controller: DashboardController, **kwargs: Any) -> None:
    """Dispatches a view to the specified controller.

    Args:
        page: The name of the page to dispatch.
        controller: The controller to dispatch the view to.
        **kwargs: Keyword arguments to pass to the view.

    Returns:
        The result of the view function.
    """
    return getattr(controller, _PAGES_VIEWS_MAP[page].__name__)(**kwargs)


def app():
    """The main function of the Streamlit app."""

    st.title("Stock Analyzer")
    st.empty()
    symbol = st.sidebar.text_input("Enter company ticker (default: AMZN)", value="AMZN")
    stock_element = st.sidebar.selectbox("Choose page", list(_PAGES_VIEWS_MAP.keys()))

    if symbol:
        st.sidebar.text(f"{symbol.upper()} provided\nYou can switch between pages!")
        controller = DashboardController(symbol)
        dispatch_view(stock_element, controller)

    if stock_element != "Home" and not symbol:
        st.write("You didn't enter correct symbol in the search box on left")


app()
