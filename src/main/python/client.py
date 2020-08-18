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
        headers = {"Content-type": "application/json",
                   "X-Finnhub-Token": self.__api_key}

        response = requests.get(
            AlphaVantageClient._URL,
            headers=headers,
            params=query_parameters,
            proxies=self.__proxy
        )

        validate_http_status(response)
        return response




