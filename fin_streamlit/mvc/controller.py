import numpy as np
import pandas as pd
import streamlit as st

from fin_streamlit.clients.alpha_vantage import AlphaVantageClient
from fin_streamlit.mvc import models, views


class DashboardController:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.client = AlphaVantageClient()

    @staticmethod
    def _clean_data_for_chart(data: pd.DataFrame) -> pd.DataFrame:
        """Cleans the given Pandas DataFrame for charting purposes.

        Args:
            data: A Pandas DataFrame containing the data to be cleaned.

        Returns:
            A Pandas DataFrame containing the cleaned data.
        """
        cleaned_data = data.drop(["reportedCurrency"])
        cols = cleaned_data.select_dtypes(exclude="int").columns.to_list()
        cleaned_data[cols] = cleaned_data[cols].astype("str")
        cleaned_data = cleaned_data.replace(["None", "0", 0], np.nan)
        return cleaned_data.dropna(how="all")

    def load_home_page(self, **kwargs):
        """Loads the home page of the dashboard.

        Args:
            **kwargs: Keyword arguments to pass to the `views.home_page_view()` function.
        """

        views.home_page_view(self.symbol)

        user_input = st.text_input("Enter company keywords that you are looking for")
        if user_input:
            data = models.search(self.client, user_input, **kwargs)
            views.search_results_view(user_input, data)

    def load_company_info(self, **kwargs):
        """Loads the company information page of the dashboard.

        Args:
            **kwargs: Keyword arguments to pass to the `models.company_info()` function.
        """

        data: dict = models.company_info(self.client, self.symbol, **kwargs)
        views.company_info_view(symbol=self.symbol, data=data)

    def load_balance_sheet(self, **kwargs):
        """Loads the balance sheet page of the dashboard.

        Args:
            **kwargs: Keyword arguments to pass to the `models.balance_sheet()` function.
        """

        data: pd.DataFrame = models.balance_sheet(self.client, self.symbol, **kwargs)
        views.balance_sheet_view(symbol=self.symbol, data=data)

        check_box = st.checkbox("Analyze Balance Sheet on Chart")
        if check_box:
            views.financial_assets_chart_view(self._clean_data_for_chart(data))

    def load_income_statement(self, **kwargs):
        """Loads the income statement page of the dashboard.

        Args:
            **kwargs: Keyword arguments to pass to the `models.income_statement()` function.
        """

        data: pd.DataFrame = models.income_statement(self.client, self.symbol, **kwargs)
        views.income_statement_view(self.symbol, data)

        check_box = st.checkbox("Analyze Income Statement on Chart")
        if check_box:
            views.financial_assets_chart_view(self._clean_data_for_chart(data))

    def load_cashflow(self, **kwargs):
        """Loads the cash flow page of the dashboard.

        Args:
            **kwargs: Keyword arguments to pass to the `models.cash_flow()` function.
        """

        data: pd.DataFrame = models.cash_flow(self.client, self.symbol, **kwargs)
        views.cash_flow_view(self.symbol, data)

        check_box = st.checkbox("Analyze Cash Flow on Chart")
        if check_box:
            views.financial_assets_chart_view(self._clean_data_for_chart(data))

    def load_quotes(self, **kwargs):
        """Loads the quotes page of the dashboard.

        Args:
            **kwargs: Keyword arguments to pass to the `models.quotes()` function.
        """

        data: pd.DataFrame = models.quotes(self.client, self.symbol, **kwargs)
        views.quotes_view(self.symbol, data)

        check_box = st.checkbox("Analyze quotes chart")
        if check_box:
            views.quotes_chart_view(data)

    def load_kpis(self, **kwargs):
        """Loads the key performance indicators (KPIs) page of the dashboard.

        Args:
            **kwargs: Keyword arguments to pass to the `models.kpis()` function.
        """

        data: pd.DataFrame = models.kpis(self.client, self.symbol, **kwargs)
        views.kpi_view(self.symbol, data)
