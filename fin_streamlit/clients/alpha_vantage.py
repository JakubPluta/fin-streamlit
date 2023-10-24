from enum import Enum
from typing import Any, List, Optional, Union

import requests
from requests.exceptions import HTTPError

from fin_streamlit.clients.utils import get_retry_session
from fin_streamlit.exc import ApiKeyMissingException
from fin_streamlit.log import get_logger
from fin_streamlit.settings import Settings

logger = get_logger(__name__)


class Endpoints(Enum):
    OVERVIEW = "OVERVIEW"
    BALANCE_SHEET = "BALANCE_SHEET"
    INCOME_STATEMENT = "INCOME_STATEMENT"
    CASH_FLOW = "CASH_FLOW"
    SYMBOL_SEARCH = "SYMBOL_SEARCH"
    TIME_SERIES_DAILY = "TIME_SERIES_DAILY"
    TIME_SERIES_WEEKLY = "TIME_SERIES_WEEKLY"
    TIME_SERIES_MONTHLY = "TIME_SERIES_MONTHLY"
    TOP_GAINERS_LOSERS = "TOP_GAINERS_LOSERS"
    EARNINGS = "EARNINGS"
    NEWS_SENTIMENT = "NEWS_SENTIMENT"


class AlphaVantageClient:
    """
    A class for interacting with the Alpha Vantage API.

    Attributes
    ----------
    base_url : str
        The base URL for the Alpha Vantage API.
    api_key : str
        The API key for the Alpha Vantage API.
    _requests_session : requests.Session
        The requests session object.
    """

    def __init__(self) -> None:
        """Initializes the Alpha Vantage client."""
        self.base_url = "https://www.alphavantage.co/query?"
        self._resolve_api_key()
        self._requests_session = get_retry_session()

    def __repr__(self) -> str:
        """Returns a string representation of the Alpha Vantage client."""
        return f"{self.__class__.__name__}"

    def _prepare_query_params(self, endpoint: str, symbol: str, **params: Any) -> dict:
        """Prepares the query parameters for the given endpoint and symbol.

        Args:
            endpoint: The Alpha Vantage API endpoint.
            symbol: The symbol to query.
            **params: Additional parameters to pass to the API.

        Returns:
            A dictionary containing the prepared query parameters.
        """

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

    def _resolve_api_key(self):
        """Resolves the Alpha Vantage API key.

        Raises:
            ApiKeyMissingException: If the Alpha Vantage API key is not found in the environment variables.
        """
        logger.debug(
            "Looking for ALPHA_VANTAGE_API_KEY key in environment variables..."
        )
        api_key = Settings.ALPHA_VANTAGE_API_KEY
        if api_key is not None and isinstance(api_key, str):
            logger.debug("ALPHA_VANTAGE_API_KEY found in environment variables")
            self.api_key = api_key
        else:
            logger.debug("ALPHA_VANTAGE_API_KEY not in environment variables")
            raise ApiKeyMissingException(
                "Please visit https://www.alphavantage.co/support/#api-key to generate api key "
                "and then pass it in .env file as ALPHA_VANTAGE_API_KEY variable"
            )

    def _make_request(
        self, endpoint: str, symbol: Optional[str] = None, **params: Any
    ) -> dict:
        """Makes a request to the Alpha Vantage API.

        Args:
            endpoint: The Alpha Vantage API endpoint.
            symbol: The symbol to query (optional).
            **params: Additional parameters to pass to the API (optional).

        Returns:
            A dictionary containing the API response.
        """

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

    def get_company_overview(self, symbol: str, **kwargs: Any) -> dict:
        """Gets the company information, financial ratios, and other key metrics for the equity specified.

        Args:
            symbol: The symbol of the company to query.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing the company overview.
        """
        return self._make_request(
            endpoint=Endpoints.OVERVIEW.value, symbol=symbol, **kwargs
        )

    def get_balance_sheet(self, symbol: str, **kwargs: Any) -> dict:
        """Gets the annual and quarterly balance sheets for the company of interest,
        with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.


        Args:
            symbol: The symbol of the company to query.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing the company balance sheet.
        """
        return self._make_request(
            endpoint=Endpoints.BALANCE_SHEET.value, symbol=symbol, **kwargs
        )

    def get_income_statement(self, symbol: str, **kwargs: Any) -> dict:
        """Gets the annual and quarterly income statements for the company of interest,
        with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.


        Args:
            symbol: The symbol of the company to query.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing the company income statement.
        """
        return self._make_request(
            endpoint=Endpoints.INCOME_STATEMENT.value, symbol=symbol, **kwargs
        )

    def get_cash_flow(self, symbol: str, **kwargs: Any) -> dict:
        """Gets the annual and quarterly cash flow statements for the company of interest,
        with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.


        Args:
            symbol: The symbol of the company to query.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing the company cash flows.
        """
        return self._make_request(
            endpoint=Endpoints.CASH_FLOW.value, symbol=symbol, **kwargs
        )

    def get_search_results(self, keywords: str, **kwargs: Any):
        """Gets the best-matching symbols and market information based on keywords of your choice.

        Args:
            keywords: A text string of your choice. For example: microsoft.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing best-matching symbols and market information based on provided keywords.
        """
        return self._make_request(
            endpoint=Endpoints.SYMBOL_SEARCH.value, keywords=keywords, **kwargs
        )

    def get_time_series_daily(
        self, symbol: str, return_full_history: bool = False, **kwargs: Any
    ) -> dict:
        """Get raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume)
        of the global equity specified, covering 20+ years of historical data.

        Args:
            symbol: The symbol of the company to query.
            return_full_history: if true returns the full-length time series of 20+ years of historical data.
                else returns last 100 data points
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing the company daily quotes
        """

        return self._make_request(
            endpoint=Endpoints.TIME_SERIES_DAILY.value,
            outputsize="full" if return_full_history else "compact",
            symbol=symbol,
            **kwargs,
        )

    def get_time_series_weekly(self, symbol: str, **kwargs: Any) -> dict:
        """Get  weekly time series (last trading day of each week, weekly open, weekly high,
        weekly low, weekly close, weekly volume) of the global equity specified,
        covering 20+ years of historical data.

        Args:
            symbol: The symbol of the company to query.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing the company daily quotes
        """
        return self._make_request(
            endpoint=Endpoints.TIME_SERIES_WEEKLY.value, symbol=symbol, **kwargs
        )

    def get_time_series_monthly(self, symbol: str, **kwargs: Any) -> dict:
        """Get monthly time series (last trading day of each month, monthly open, monthly high,
        monthly low, monthly close, monthly volume) of the global equity specified,
        covering 20+ years of historical data.

        Args:
            symbol: The symbol of the company to query.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing the company daily quotes
        """
        return self._make_request(
            endpoint=Endpoints.TIME_SERIES_MONTHLY.value, symbol=symbol, **kwargs
        )

    def get_top_gainers_and_losers(self, **kwargs: Any):
        """Gets top 20 gainers, losers, and the most active traded tickers in the US market.

        Args:
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing the company earnings.
        """
        return self._make_request(endpoint=Endpoints.TOP_GAINERS_LOSERS.value, **kwargs)

    def get_earnings(self, symbol: str, **kwargs: Any):
        """Gets annual and quarterly earnings (EPS) for the company of interest.
        Quarterly data also includes analyst estimates and surprise metrics.

        Args:
            symbol: The symbol of the company to query.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing the company earnings.
        """
        return self._make_request(
            endpoint=Endpoints.EARNINGS.value, symbol=symbol, **kwargs
        )

    def get_market_news_sentiment(
        self,
        symbol: str,
        topics: Optional[Union[List[str], str]] = None,
        limit: int = 50,
        **kwargs,
    ) -> dict:
        """Get live and historical market news & sentiment data

        Args:
            symbol: The symbol of the company to query.
            topics: The news topics of your choice.
                Blockchain: blockchain
                Earnings: earnings
                IPO: ipo
                Mergers & Acquisitions: mergers_and_acquisitions
                Financial Markets: financial_markets
                Economy - Fiscal Policy (e.g., tax reform, government spending): economy_fiscal
                Economy - Monetary Policy (e.g., interest rates, inflation): economy_monetary
                Economy - Macro/Overall: economy_macro
                Energy & Transportation: energy_transportation
                Finance: finance
                Life Sciences: life_sciences
                Manufacturing: manufacturing
                Real Estate & Construction: real_estate
                Retail & Wholesale: retail_wholesale
                Technology: technology
            limit: he number of results to return
            **kwargs: Additional parameters to pass to the API.

        Returns:
            A dictionary containing market news and sentiments data
        """

        if topics is not None:
            topics = ",".join(topics) if isinstance(topics, list) else topics
            return self._make_request(
                endpoint=Endpoints.NEWS_SENTIMENT.value,
                tickers=symbol,
                topics=topics,
                limit=limit,
                **kwargs,
            )

        return self._make_request(
            endpoint=Endpoints.NEWS_SENTIMENT.value,
            tickers=symbol,
            limit=limit,
            **kwargs,
        )
