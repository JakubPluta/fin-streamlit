from typing import Any

import pandas as pd

from fin_streamlit.clients.alpha_vantage import AlphaVantageClient
import streamlit as st

from fin_streamlit.utils import _prepare_statement_df

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


@st.cache_data
def _company_info(_client: AlphaVantageClient, symbol: str, **kwargs: Any) -> dict:
    """Gets an overview of a company, cached in Streamlit.

    Args:
        _client: An AlphaVantageClient.
        symbol: The symbol of the company to query.
        **kwargs: Additional parameters to pass to the API.

    Returns:
        A dictionary containing the company overview.
    """
    data = _client.get_company_overview(symbol, **kwargs)
    return data


@st.cache_data
def company_info(_client: AlphaVantageClient, symbol: str, **kwargs: Any) -> dict:
    """Gets an overview of a company, cached in Streamlit

    Args:
        _client: An AlphaVantageClient.
        symbol: The symbol of the company to query.
        **kwargs: Additional parameters to pass to the API.

    Returns:
        A dictionary containing the company's basic information, such as its
        name, description, industry

    """
    data = _company_info(_client, symbol, **kwargs)
    return {
        k: v
        for k, v in data.items()
        if k in [*COMPANY_BASIC_INFORMATION, *["Name", "Description"]]
    }


@st.cache_data
def balance_sheet(
    _client: AlphaVantageClient, symbol: str, **kwargs: Any
) -> pd.DataFrame:
    """Gets the balance sheet for a company, cached in Streamlit, and returns a Pandas DataFrame.

    Args:
        _client: An AlphaVantageClient.
        symbol: The symbol of the company to query.
        **kwargs: Additional parameters to pass to the API.

    Returns:
        A Pandas DataFrame containing the company's balance sheet data.
    """
    data: dict = _client.get_balance_sheet(symbol=symbol, **kwargs).get("annualReports")
    return _prepare_statement_df(data)


@st.cache_data
def income_statement(
    _client: AlphaVantageClient, symbol: str, **kwargs: Any
) -> pd.DataFrame:
    """Gets the income statement for a company, cached in Streamlit, and returns a Pandas DataFrame.

    Args:
        _client: An AlphaVantageClient.
        symbol: The symbol of the company to query.
        **kwargs: Additional parameters to pass to the API.

    Returns:
        A Pandas DataFrame containing the company's income statement data.
    """
    data: dict = _client.get_income_statement(symbol, **kwargs).get("annualReports")
    return _prepare_statement_df(data)


@st.cache_data
def cash_flow(_client: AlphaVantageClient, symbol: str, **kwargs: Any) -> pd.DataFrame:
    """Gets the cash flow for a company, cached in Streamlit, and returns a Pandas DataFrame.

    Args:
        _client: An AlphaVantageClient.
        symbol: The symbol of the company to query.
        **kwargs: Additional parameters to pass to the API.

    Returns:
        A Pandas DataFrame containing the company's cash flow data.
    """
    data: dict = _client.get_cash_flow(symbol, **kwargs).get("annualReports")
    return _prepare_statement_df(data)


@st.cache_data
def quotes(_client: AlphaVantageClient, symbol: str, **kwargs: Any) -> pd.DataFrame:
    """Gets the daily quotes for a company, cached in Streamlit, and returns a Pandas DataFrame.

    Args:
        _client: An AlphaVantageClient.
        symbol: The symbol of the company to query.
        **kwargs: Additional parameters to pass to the API.

    Returns:
        A Pandas DataFrame containing the company's daily quote data.
    """
    data: dict = _client.get_time_series_daily(symbol, **kwargs)
    data = data.get("Time Series (Daily)")
    df = pd.DataFrame(data).T.reset_index()
    df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    return df


@st.cache_data
def kpis(_client: AlphaVantageClient, symbol: str, **kwargs: Any) -> pd.DataFrame:
    """Gets the key performance indicators (KPIs) for a company, cached in Streamlit,
    and returns a Pandas DataFrame.

    Args:
        _client: An AlphaVantageClient.
        symbol: The symbol of the company to query.
        **kwargs: Additional parameters to pass to the API.

    Returns:
        A Pandas DataFrame containing the company's KPI data.

    """
    data: dict = _company_info(_client, symbol, **kwargs)
    _to_remove = [
        *COMPANY_BASIC_INFORMATION,
        *[
            "Symbol",
            "AssetType",
            "Description",
            "Name",
            "FiscalYearEnd",
            "LatestQuarter",
        ],
    ]

    table_dict = {k: v for k, v in data.items() if k not in _to_remove}
    df = pd.DataFrame(table_dict.items())
    df.columns = ["Label", "Value"]
    return df
