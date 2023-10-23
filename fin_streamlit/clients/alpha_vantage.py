
import os

import requests

from fin_streamlit.clients.utils import get_retry_session
from fin_streamlit.exc import ApiKeyMissingException
from typing import Optional, List, Any, Union
from fin_streamlit.log import get_logger
from requests.exceptions import HTTPError


logger = get_logger(__name__)


class AlphaVantageClient:
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://www.alphavantage.co/query?"
        self.api_key = api_key
        self._requests_session = get_retry_session()

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def _prepare_query_params(self, endpoint: str, symbol: str, **params):
        qp = {
            **{"function": endpoint, "apikey": self.api_key},
            **params,
        }
        if symbol is not None:
            qp["symbol"] = symbol
        return qp

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
                logger.info("ALPHA_VANTAGE_API_KEY found in environment variables")
            except KeyError:
                logger.error("ALPHA_VANTAGE_API_KEY not in environment variables")
                raise ApiKeyMissingException(
                    "Please visit https://www.alphavantage.co/support/#api-key to generate api key "
                    "and then pass it via api_key parameter or set ALPHA_VANTAGE_API_KEY env variable"
                )

    def _make_request(self, endpoint: str, symbol: Optional[str] = None, **params: Any) -> dict:
        query_params = self._prepare_query_params(
            endpoint=endpoint, symbol=symbol, **params
        )
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

    def get_company_overview(self, symbol, **kwargs):
        return self._make_request(endpoint="OVERVIEW", symbol=symbol, **kwargs)

    def get_balance_sheet(self, symbol, **kwargs):
        return self._make_request(endpoint="BALANCE_SHEET", symbol=symbol, **kwargs)

    def get_income_statement(self, symbol, **kwargs):
        return self._make_request(endpoint="INCOME_STATEMENT", symbol=symbol, **kwargs)

    def get_cash_flow(self, symbol, **kwargs):
        return self._make_request(endpoint="CASH_FLOW", symbol=symbol, **kwargs)

    def get_search_results(self, keywords: str, **kwargs):
        return self._make_request(endpoint="SYMBOL_SEARCH", keywords=keywords, **kwargs)

    def get_time_series_daily(
        self, symbol: str, return_full_history: bool = False, **kwargs
    ):
        return self._make_request(
            endpoint="TIME_SERIES_DAILY",
            outputsize="full" if return_full_history else "compact",
            symbol=symbol,
            **kwargs,
        )

    def get_time_series_weekly(self, symbol: str, **kwargs):
        return self._make_request(
            endpoint="TIME_SERIES_WEEKLY", symbol=symbol, **kwargs
        )

    def get_time_series_monthly(self, symbol: str, **kwargs):
        return self._make_request(
            endpoint="TIME_SERIES_MONTHLY", symbol=symbol, **kwargs
        )

    def get_top_gainers_and_losers(self, symbol: str, **kwargs):
        return self._make_request(
            endpoint="TOP_GAINERS_LOSERS", symbol=symbol, **kwargs
        )

    def get_earnings(self, symbol: str, **kwargs):
        return self._make_request(endpoint="EARNINGS", symbol=symbol, **kwargs)

    def get_market_news_sentiment(
        self,
        symbol: str,
        topics: Optional[Union[List[str], str]] = None,
        limit: int = 50,
        **kwargs,
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
                tickers=symbol,
                topics=topics,
                limit=limit,
                **kwargs
            )

        return self._make_request(
            endpoint="NEWS_SENTIMENT", tickers=symbol, limit=limit, **kwargs
        )
