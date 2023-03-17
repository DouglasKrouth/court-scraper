from court_scraper.base.selenium_site import SeleniumSite
from datetime import date
from court_scraper.utils import dates_for_range, get_captcha_service_api_key


class SearchConfigurationError(Exception):
    pass


class Site(SeleniumSite):
    """
    Based on the configuration of the SF Court portal website, we can pass a CAPTCHA once which will
    give us a single session token. This session token will then be used with the 'requests' package to generate
    the following ["case number", "date generated", "case title"]
    """

    current_day = date.today().strftime("%Y-%m-%d")

    def __init__(self, captcha_api_key=None):
        self.captcha_api_key = captcha_api_key or get_captcha_service_api_key()
        self.url = r"https://webapps.sftc.org/captcha/captcha.dll?referrer=https://webapps.sftc.org/ci/CaseInfo.dll?"

    def __repr__(self):
        return f"San Francisco Court Scraper ({self.current_day})"

    def search_by_date(
        self, start_date=None, end_date=None, download_dir=None, headless=True
    ):
        """
        The SF Court portal site only allows for search by ind. dates.
        We'll create a range with start, end dates if specified.
        Args:
            start_date (str): start date in YYYY-MM-DD format (optional)
            end_date (str): end date in YYYY-MM-DD format (optional)
            download_dir (str): Override Selenium download directory (defaults to standard court-scraper)
            headless (boolean): Run Selenium in headless mode for case number search (defaults to True)

        Returns:
            List of tuples containing ("case number", "date generated", "case title")
        """
        self.download_dir = download_dir or self.get_download_dir()
        self.driver = self._init_chrome_driver(headless=headless)
        self.driver.get(self.url)
