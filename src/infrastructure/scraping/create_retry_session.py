import requests
from requests.adapters import HTTPAdapter, Retry


class TimeoutHTTPAdapter(HTTPAdapter):
    """
    Custom HTTPAdapter to handle timeouts and retries.
    """
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop('timeout', 10)
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        return super().send(request, **kwargs)


def create_retry_session(retries: int = 3, backoff_factor: float = 0.5, status_forcelist: tuple = (500, 502, 503, 504), timeout: int = 10) -> requests.Session:
    """
    Create a requests session with retry logic.
    """
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist
    )
    adapter = TimeoutHTTPAdapter(max_retries=retry, timeout=timeout)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session