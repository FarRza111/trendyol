"""
Test module for scraperABC.py
Tests the ScraperABC class methods
"""
import pytest
from unittest.mock import Mock, patch
import requests
from scraperABC import ScraperABC


class TestScraperABC:
    """Test cases for the ScraperABC class"""

    @pytest.fixture
    def scraper(self):
        """Create a ScraperABC instance for testing"""
        return ScraperABC()

    def test_check_status_code_success(self, scraper):
        """Test check_status_code with successful response (200)"""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        
        result = scraper.check_status_code(mock_response)
        assert result is True

    def test_check_status_code_failure(self, scraper):
        """Test check_status_code with failed response (404)"""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 404
        
        result = scraper.check_status_code(mock_response)
        assert result is False

    def test_check_status_code_server_error(self, scraper):
        """Test check_status_code with server error (500)"""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 500
        
        result = scraper.check_status_code(mock_response)
        assert result is False

    @patch('scraperABC.requests.get')
    def test_health_check_success(self, mock_get, scraper):
        """Test health_check with successful response"""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = scraper.health_check("https://example.com")
        
        assert result["status"] == "healthy"
        assert result["status_code"] == 200
        assert result["error"] is None
        assert result["response_time"] is not None
        assert result["timestamp"] is not None

    @patch('scraperABC.requests.get')
    def test_health_check_unhealthy(self, mock_get, scraper):
        """Test health_check with unhealthy response (404)"""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = scraper.health_check("https://example.com")
        
        assert result["status"] == "unhealthy"
        assert result["status_code"] == 404

    @patch('scraperABC.requests.get')
    def test_health_check_request_exception(self, mock_get, scraper):
        """Test health_check when request raises an exception"""
        mock_get.side_effect = requests.RequestException("Connection error")
        
        result = scraper.health_check("https://example.com", max_retries=1)
        
        assert result["status"] == "unhealthy"
        assert result["error"] is not None
        assert "Connection error" in result["error"]

    @patch('scraperABC.requests.get')
    @patch('scraperABC.time.sleep')
    def test_health_check_retry_logic(self, mock_sleep, mock_get, scraper):
        """Test health_check retry logic on failures"""
        # First two attempts fail, third succeeds
        mock_response_fail = Mock(spec=requests.Response)
        mock_response_fail.status_code = 500
        mock_response_success = Mock(spec=requests.Response)
        mock_response_success.status_code = 200
        
        mock_get.side_effect = [mock_response_fail, mock_response_fail, mock_response_success]
        
        result = scraper.health_check("https://example.com", max_retries=3)
        
        assert result["status"] == "healthy"
        assert mock_get.call_count == 3
        assert mock_sleep.call_count == 2  # Sleep between retries

    @patch('scraperABC.requests.get')
    def test_health_check_with_custom_timeout(self, mock_get, scraper):
        """Test health_check with custom timeout parameter"""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = scraper.health_check("https://example.com", timeout=5)
        
        assert result["status"] == "healthy"
        mock_get.assert_called_once()
        # Check that timeout was passed to requests.get
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["timeout"] == 5

    def test_scrape_method_exists(self, scraper):
        """Test that scrape method exists and can be called"""
        # The method should exist but returns None (abstract method stub)
        result = scraper.scrape()
        assert result is None

    def test_fetch_page_method_exists(self, scraper):
        """Test that fetch_page method exists"""
        result = scraper.fetch_page("https://example.com")
        assert result is None

    def test_create_soup_method_exists(self, scraper):
        """Test that create_soup method exists"""
        result = scraper.create_soup("<html></html>", "html.parser")
        assert result is None
