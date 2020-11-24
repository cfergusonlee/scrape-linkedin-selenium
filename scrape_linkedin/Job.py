from .utils import *
from .ResultsObject import ResultsObject
from bs4 import BeautifulSoup
import re


class Job(ResultsObject):
    """Linkedin Job Page Object"""

    attributes = [
        "details",
    ]

    def __init__(self, details):
        self.details_soup = BeautifulSoup(details, "html.parser")

    @property
    def details(self):
        """Return dict of the details section of the Linkedin Page"""

        # Banner containing job name + location
        headline_selector = ".justify-space-between.align-items-stretch"
        headline_container = one_or_default(self.details_soup, headline_selector)
        headline_details = self.get_headline_details(headline_container)

        # Main container with job description details
        description_selector = ".jobs-box--fadein"
        description_container = one_or_default(self.details_soup, description_selector)
        description_details = self.get_description_details(description_container)

        return {**headline_details, **description_details}

    def get_headline_details(self, headline_container):
        """
        Args:
            headline_container:

        Returns:
            Dict of job headline details. These include:
                - job_title
                - location
                - organization
        """
        job_title_selector = ".jobs-top-card__job-title"
        location_selector = ".jobs-top-card__bullet"
        organization_selector = ".jobs-top-card__company-url"
        headline_details = get_info(
            headline_container,
            {
                "job_title": job_title_selector,
                "location": location_selector,
                "organization": organization_selector,
            },
        )
        return headline_details

    def get_description_details(self, description_container):
        """
        Args:
            description_container:

        Returns:
            Dict of job description details. These include:
                - Seniority
                - Industries
                - Employment Type
                - Job Functions
                - Job Description
        """

        # Parse job description
        job_description_selector = ".jobs-box__html-content"
        job_description = text_or_default(
            description_container, job_description_selector
        )
        description_details = {"job_description": job_description}

        # Parse remaining details from job details box
        description_boxes_selector = ".jobs-description-details .jobs-box__group"
        description_boxes = all_or_default(
            description_container, description_boxes_selector
        )
        for description_box in description_boxes:
            description_title_selector = "h3"
            description_title = text_or_default(
                description_box, description_title_selector
            ).replace("Industry", "Industries")
            description_key = "_".join(description_title.lower().split())
            if description_key in ("seniority_level", "employment_type"):
                description_value_selector = "p"
            else:
                description_value_selector = ".jobs-description-details__list-item"

            description_value_elements = all_or_default(
                description_box, description_value_selector
            )
            description_value = [
                element.get_text(strip=True) for element in description_value_elements
            ]
            if len(description_value) == 1:
                description_value = description_value[0]
            description_details[description_key] = description_value

        return description_details
