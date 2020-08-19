import os
import requests
from utils import *


ENDPOINTS = {
    "OVERVIEW" : "OVERVIEW",
    "INCOME_STATEMENT" : "INCOME_STATEMENT",
    "BALANCE_SHEET" : "BALANCE_SHEET",
    "CASH_FLOW" : "CASH_FLOW",

}


class AlphaVantageClient:

    _URL = "https://www.alphavantage.co/query?"

    def __init__(self, api_key=None):
        self.__api_key = api_key
        self.__proxy = {}
        self.__validate_api_key()
        self.__data_type = 'json'

    def __validate_api_key(self, env="ALPHA_API_KEY"):
        if not self.__api_key:
            self.__api_key = os.environ.get(env)
        if self.__api_key is None or not isinstance(self.__api_key, str):
            raise ValueError(
                "Please visit \n" "https://www.alphavantage.co/support/#api-key\n and get your free API KEY")

    def show_base_url(self):
        print(self._URL)

    def set_proxy(self, proxy=None):
        """sample format of proxy: 'http://<user>:<pass>@<proxy>:<port>'

        More about setting proxies with requests library:
        proxies = {
          'http': 'http://10.10.1.10:3128',
          'https': 'http://10.10.1.10:1080',
        }

        requests.get('http://example.org', proxies=proxies)

        """
        self.__proxy = proxy

    def get_proxy(self):
        return self.__proxy

    def __call_api(self, query_parameters: dict,**kwargs):
        """
        The structure looks like:
            co./query?function{}&symbol{}
        :param query_parameters:
        :return: response
        """
        query_parameters["apikey"] = self.__api_key

        response = requests.get(
            AlphaVantageClient._URL,
            params=query_parameters,
            proxies=self.__proxy
        )

        validate_http_status(response)
        return response.json()

    def company_overview(self, ticker: str, **kwargs):
        query_parameters = {
            "function": "OVERVIEW",
            "symbol": ticker
        }
        return self.__call_api(query_parameters, **kwargs)

    def balance_sheet(self, ticker: str, **kwargs):
        query_parameters = {
            "function": "BALANCE_SHEET",
            "symbol": ticker
        }
        return self.__call_api(query_parameters, **kwargs)

    def income_statement(self, ticker: str, **kwargs):
        query_parameters = {
            "function": "INCOME_STATEMENT",
            "symbol": ticker
        }
        return self.__call_api(query_parameters, **kwargs)

    def cash_flow(self, ticker: str, **kwargs):
        query_parameters = {
            "function": "CASH_FLOW",
            "symbol": ticker
        }
        return self.__call_api(query_parameters, **kwargs)

    def search(self, keywords: str, **kwargs):
        query_parameters = {
            "function": "SYMBOL_SEARCH",
            "keywords": keywords
        }
        return self.__call_api(query_parameters, **kwargs)

    def time_series_daily(self, symbol: str, **kwargs):
        query_parameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize" : "full"
        }
        return self.__call_api(query_parameters, **kwargs)

    def time_series_monthly(self, symbol: str, **kwargs):
        query_parameters = {
            "function": "TIME_SERIES_MONTHLY",
            "symbol": symbol,
            "outputsize" : "full"
        }
        return self.__call_api(query_parameters, **kwargs)

    def time_series_weekly(self, symbol: str, **kwargs):
        query_parameters = {
            "function": "TIME_SERIES_WEEKLY",
            "symbol": symbol,
            "outputsize" : "full"
        }
        return self.__call_api(query_parameters, **kwargs)


