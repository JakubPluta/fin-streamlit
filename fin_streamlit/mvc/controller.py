from fin_streamlit.clients.alpha_vantage import AlphaVantageClient
from fin_streamlit.utils import clean_data
from fin_streamlit.mvc import views as views
from fin_streamlit.mvc import models as models
import streamlit as st
import pandas as pd


class DashboardController:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.client = AlphaVantageClient()

    def load_home_page(self, **kwargs):
        views.home_page_view(self.symbol)

    def load_company_info(self, **kwargs):
        data: dict = models.company_info(self.client, self.symbol, **kwargs)
        views.company_info_view(symbol=self.symbol, data=data)

    def load_balance_sheet(self, **kwargs):
        df: pd.DataFrame = models.balance_sheet(self.client, self.symbol, **kwargs)
        views.balance_sheet_view(symbol=self.symbol, data=df)
        df = clean_data(df, ["reportedCurrency"])
        categories = df.index.to_list()
        chart = st.checkbox("Analyze Balance Sheet on Chart")
        views.balance_sheet_chart_view(chart, df, categories)

    def load_income_statement(self, **kwargs):
        data: pd.DataFrame = models.income_statement(self.client, self.symbol, **kwargs)
        views.income_statement_view(self.symbol, data)

        data = clean_data(data, ["reportedCurrency"])
        categories = data.index.to_list()
        chart = st.checkbox("Analyze Income Statement on Chart")
        views.income_statement_chart_view(chart, data, categories)

    def load_cashflow(self, **kwargs):
        data: pd.DataFrame = models.cash_flow(self.client, self.symbol, **kwargs)
        views.cash_flow_view(self.symbol, data)

        data = clean_data(data, ["reportedCurrency"])
        categories = data.index.to_list()
        chart = st.checkbox("Analyze Income Statement on Chart")
        views.cash_flow_chart_view(chart, data, categories)

    def load_quotes(self, **kwargs):
        data: pd.DataFrame = models.quotes(self.client, self.symbol, **kwargs)
        views.quotes_view(self.symbol, data)

        chart = st.checkbox("Press if you want to show chart")
        if chart:
            views.quotes_chart_view(data)

    def load_kpis(self, **kwargs):
        data = pd.DataFrame = models.kpis(self.client, self.symbol, **kwargs)
        views.kpi_view(self.symbol, data)
