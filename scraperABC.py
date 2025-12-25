from abc import abstractmethod
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import time


class ScraperABC:

    # @abstractmethod
    def scrape(self):
        pass

    def fetch_page(self, url) -> str:
        pass

    def create_soup(self, raw_html, parser) -> BeautifulSoup:
        pass

    def check_status_code(self, response: requests.Response) -> bool:
        """
        Check if the HTTP response status code is 200 (OK).
        """
        return response.status_code == 200

    def health_check(self, url: str, max_retries: int = 3, timeout: int = 10) -> Dict[str, any]:
        """
        Perform a health check on the target URL

        Args:
            url (str): The URL to check
            max_retries (int): Maximum number of retry attempts
            timeout (int): Timeout in seconds for each request

        Returns:
            Dict containing health check results
        """
        results = {
            "status": "unhealthy",
            "response_time": None,
            "status_code": None,
            "error": None,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        for attempt in range(max_retries):
            try:
                start_time = time.time()
                response = requests.get(url, timeout=timeout)
                response_time = time.time() - start_time

                results.update({
                    "status": "healthy" if self.check_status_code(response) else "unhealthy",
                    "response_time": f"{response_time:.2f}s",
                    "status_code": response.status_code,
                    "error": None
                })

                if results["status"] == "healthy":
                    break

            except requests.RequestException as e:
                results.update({
                    "error": str(e),
                    "status": "unhealthy"
                })

            if attempt < max_retries - 1:
                time.sleep(1)  # Wait 1 second between retries

        return results

