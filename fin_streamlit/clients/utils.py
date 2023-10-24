import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def get_retry_session(retries=6, backoff_factor=0.1) -> requests.Session:
    """Get a Session object with retry capabilities.

    Args:
        retries: The number of retries to attempt before giving up.
        backoff_factor: The factor by which to increase the wait time between retries.

    Returns:
        A Session object with retry capabilities.
    """
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.mount("https://www.alphavantage.co", adapter)
    return session
