from .Scraper import Scraper
from .ConnectionScraper import ConnectionScraper
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time
from .Job import Job
from .utils import AnyEC


class JobScraper(Scraper):
    """
    Scraper for LinkedIn Job postings. See inherited Scraper class for
    details about the constructor.
    """

    MAIN_SELECTOR = ".core-rail"
    ERROR_SELECTOR = ".global-error"

    def scrape(self, job_id):
        self.load_job_page(job_id)
        return self.get_job()

    def load_job_page(self, job_id):
        url = f"https://www.linkedin.com/jobs/view/{job_id}"
        self.driver.get(url)
        # Wait for page to load dynamically via javascript
        try:
            myElem = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.MAIN_SELECTOR))
            )
        except TimeoutException as e:
            raise ValueError(
                """Took too long to load profile.  Common problems/solutions:
                1. Invalid LI_AT value: ensure that yours is correct (they
                   update frequently)
                2. Slow Internet: increase the time out parameter in the Scraper
                   constructor
                3. Job Posting Unavailable: Job Posting link does not match any 
                   current Linkedin Job Postings
                """
            )
        # Scroll to the bottom of the page incrementally to load any lazy-loaded content
        self.scroll_to_bottom()
        self.expand_job_description()

    def get_job(self):
        details_html = self.driver.page_source
        return Job(details=details_html)

    def expand_job_description(self):
        """
        Expands job description text if necessary
        Returns:

        """
        try:
            description_expansion_selector = 'button[data-control-name="view_less"]'
            description_expansion_button = self.driver.find_element_by_css_selector(
                description_expansion_selector
            )
            # Scrolls the desired element into view
            self.driver.execute_script(
                "arguments[0].scrollIntoView(false);", description_expansion_button
            )
            description_expansion_button.click()
        except:
            pass
