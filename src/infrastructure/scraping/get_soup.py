# src/infrastructure/scraping/get_soup.py
# -*- coding: utf-8 -*-

import time
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError

from bs4 import BeautifulSoup

from settings import logger


class GetSoup:
    """
    Class to handle the creation of a BeautifulSoup object from a URL.
    """
    def __init__(self, url: str, session, timeout: int = 10):
        """
        Get the BeautifulSoup object from the URL.
        """
        local_url = url
        try:
            response = session.get(local_url, timeout=timeout)
            logger.debug(f"URL: {local_url}, Status Code: {response.status_code}")
            time.sleep(1)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.content, 'lxml')
            self.soup = soup
        except HTTPError as e:
            logger.error(f"HTTP error occurred. @get_soup {local_url}: {e}", exc_info=True)
            raise e
        except ConnectionError as e:
            logger.error(f"Connection error occurred. @get_soup {local_url}: {e}", exc_info=True)
            raise e
        except Timeout as e:
            logger.error(f"Timeout error occurred. @get_soup {local_url}: {e}", exc_info=True)
            raise e
        except RequestException as e:
            logger.error(f"Request error occurred. @get_soup {local_url}: {e}", exc_info=True)
            raise e
        except Exception as e:
            logger.error(f"An unexpected error occurred. @get_soup {local_url}: {e}", exc_info=True)
            raise e
        
    
    def select(self, selectors: list[str]) -> list:
        """
        Select elements from the soup using a CSS selector.
        """
        try:
            for selector in selectors:
                elements = self.soup.select(selector)
                if elements:
                    return elements
            logger.warning(f"No elements found for selectors: {selectors}")
            return []
        except Exception as e:
            logger.error(f"Error occurred while selecting elements: {e}", exc_info=True)
            return []
        
    
    def select_one(self, selectors: list[str]):
        """
        Select a single element from the soup using a CSS selector.
        """
        try:
            for selector in selectors:
                element = self.soup.select_one(selector)
                if element:
                    return element
            logger.warning(f"No elements found for selectors: {selectors}")
            return None
        except Exception as e:
            logger.error(f"Error occurred while selecting elements: {e}", exc_info=True)
            return None