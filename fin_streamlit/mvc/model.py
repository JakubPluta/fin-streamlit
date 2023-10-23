import pandas as pd

from fin_streamlit.clients.alpha_vantage import AlphaVantageClient
import streamlit as st

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
def _company_info(_client: AlphaVantageClient, symbol, **kwargs):
    data = _client.get_company_overview(symbol, **kwargs)
    return data


@st.cache_data
def company_info(_client: AlphaVantageClient, symbol, **kwargs):
    data = _company_info(_client, symbol, **kwargs)
    return {
        k: v
        for k, v in data.items()
        if k in [*COMPANY_BASIC_INFORMATION, *["Name", "Description"]]
    }


@st.cache_data
def balance_sheet(_client: AlphaVantageClient, symbol, **kwargs):
    data: dict = _client.get_balance_sheet(symbol=symbol, **kwargs)
    data = data.get("annualReports")
    df = pd.json_normalize(data).T
    df.columns = df.iloc[0]
    df = df[1:]
    return df


@st.cache_data
def income_statement(_client: AlphaVantageClient, symbol, **kwargs):
    data: dict = _client.get_income_statement(symbol, **kwargs)
    data = data.get("annualReports")
    df = pd.json_normalize(data).T
    df.columns = df.iloc[0]
    df = df[1:]
    return df


@st.cache_data
def cash_flow(_client: AlphaVantageClient, symbol, **kwargs):
    data: dict = _client.get_cash_flow(symbol, **kwargs)
    data = data.get("annualReports")
    df = pd.json_normalize(data).T
    df.columns = df.iloc[0]
    df = df[1:]
    return df


@st.cache_data
def quotes(_client: AlphaVantageClient, symbol, **kwargs):
    data: dict = _client.get_time_series_daily(symbol, **kwargs)
    data = data.get("Time Series (Daily)")
    df = pd.DataFrame(data).T.reset_index()
    df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    return df


@st.cache_data
def kpis(_client: AlphaVantageClient, symbol, **kwargs):
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