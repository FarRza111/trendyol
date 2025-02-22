from abc import abstractmethod


class ScraperABC:

    # @abstractmethod
    def scrape(self):
        pass

    def fetch_page(self, url) -> str:
        pass

    def create_soup(self, raw_html, parser) -> BeautifulSoup:
        pass


