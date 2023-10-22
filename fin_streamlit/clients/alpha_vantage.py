import os

import requests

from fin_streamlit.clients.utils import get_retry_session
from fin_streamlit.exc import ApiKeyMissingException
from typing import Optional, List, Any, Union
from fin_streamlit.log import get_logger
from requests.exceptions import HTTPError


logger = get_logger(__name__)


class AlphaVantageClient:
    def __init__(self, symbol: Optional[str], api_key: Optional[str] = None):
        self.base_url = "https://www.alphavantage.co/query?"
        self.api_key = api_key
        self.symbol = symbol
        self._requests_session = get_retry_session()

    def __repr__(self):
        return f"{self.__class__.__name__}(symbol={self.symbol})"

    def _prepare_query_params(self, endpoint: str, **params):
        return {
            **{"function": endpoint, "symbol": self.symbol, "apikey": self.api_key},
            **params,
        }

    @property
    def _session(self) -> requests.Session:
        """Returns the request session object."""
        return self._requests_session

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str):
        if api_key and isinstance(api_key, str):
            self._api_key = api_key
        else:
            logger.info(
                "AlphaVantage api key not set when initializing AlphaVantageClient. "
                "Looking for ALPHA_VANTAGE_API_KEY key in environment variables..."
            )
            try:
                self._api_key = os.environ["ALPHA_VANTAGE_API_KEY"]
            except KeyError:
                logger.error("ALPHA_VANTAGE_API_KEY not in environment variables")
                raise ApiKeyMissingException(
                    "Please visit https://www.alphavantage.co/support/#api-key to generate api key "
                    "and then pass it via api_key parameter or set ALPHA_VANTAGE_API_KEY env variable"
                )

    def _make_request(self, endpoint: str, **params: Any) -> dict:
        query_params = self._prepare_query_params(endpoint=endpoint, **params)
        try:
            return self._session.get(
                self.base_url,
                params=query_params,
            ).json()
        except HTTPError as he:
            logger.error("Invalid HTTP response. Error: %s", str(he))
        except Exception as e:
            logger.error("Couldn't make request: Error: %s", str(e))
        return {}

    def get_company_overview(self, **kwargs):
        return self._make_request(endpoint="OVERVIEW", **kwargs)

    def get_balance_sheet(self, **kwargs):
        return self._make_request(endpoint="BALANCE_SHEET", **kwargs)

    def get_income_statement(self, **kwargs):
        return self._make_request(endpoint="INCOME_STATEMENT", **kwargs)

    def get_cash_flow(self, **kwargs):
        return self._make_request(endpoint="CASH_FLOW", **kwargs)

    def get_search_results(self, keywords: str, **kwargs):
        return self._make_request(endpoint="SYMBOL_SEARCH", keywords=keywords, **kwargs)

    def get_time_series_daily(self, return_full_history: bool = False, **kwargs):
        return self._make_request(
            endpoint="TIME_SERIES_DAILY",
            outputsize="full" if return_full_history else "compact",
            **kwargs,
        )

    def get_time_series_weekly(self, **kwargs):
        return self._make_request(endpoint="TIME_SERIES_WEEKLY", **kwargs)

    def get_time_series_monthly(self, **kwargs):
        return self._make_request(endpoint="TIME_SERIES_MONTHLY", **kwargs)

    def get_top_gainers_and_losers(self, **kwargs):
        return self._make_request(endpoint="TOP_GAINERS_LOSERS", **kwargs)

    def get_earnings(self, **kwargs):
        return self._make_request(endpoint="EARNINGS", **kwargs)

    def get_market_news_sentiment(
        self, topics: Optional[Union[List[str], str]] = None, limit: int = 50, **kwargs
    ):
        supported_topics = [
            "earnings",
            "ipo",
            "mergers_and_acquisitions",
            "financial_markets",
            "economy_fiscal",
            "economy_monetary",
            "economy_macro",
            "energy_transportation",
            "finance",
            "life_sciences",
            "manufacturing",
            "real_estate",
            "retail_wholesale",
            "technology",
        ]
        topics = ",".join(topics) if topics and isinstance(topics, list) else topics

        if topics is not None:
            ",".join(topics) if isinstance(topics, list) else topics
            return self._make_request(
                endpoint="NEWS_SENTIMENT",
                tickers=self.symbol,
                topics=topics,
                limit=limit,
            )

        return self._make_request(
            endpoint="NEWS_SENTIMENT", tickers=self.symbol, limit=limit
        )
