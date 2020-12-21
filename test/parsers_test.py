from scrape_linkedin import Company, Profile, Job
from os import path
import bs4
from bs4 import BeautifulSoup as BS

DIR = path.dirname(path.abspath(__file__))


def test_company_overview():
    expected_overview = {
        "name": "Facebook",
        "num_employees": 77893,
        "type": "Public Company",
        "company_size": "10,001+ employees",
        "specialties": "Connectivity, Artificial Intelligence, Virtual Reality, Machine Learning, Social Media, Augmented Reality, Marketing Science, Mobile Connectivity, and Open Compute",
        "founded": "2004",
        "industry": "Internet",
        "headquarters": "Menlo Park, CA",
        "website": "http://www.facebook.com/careers",
        "image": "./(72) Facebook_ About _ LinkedIn_files/0(2)",
    }
    with open(path.join(DIR, "html_files/facebook_overview.html"), "r") as f:
        company = Company(f.read(), "", "", "").to_dict()
    for key in expected_overview:
        assert expected_overview[key] == company["overview"][key]


def test_job_details():
    expected_details = {
        "job_title": "Data Analyst",
        "location": "Weatogue, CT",
        "organization": "US Tech Solutions",
        "seniority_level": "Mid-Senior level",
        "industries": "Information Technology & Services",
        "employment_type": "Contract",
        "job_functions": "Information Technology",
        "job_description": """Job Description US Tech Solutions is seeking a “Data Analyst” for a 3- 6 months contract to Hire position with a client in Weatogue, CT Description: Insurance Data Experience: Experience with Insurance Data Systems- for Submission, Policy/Premium or Claims level analysis Multiple tools: PowerBI, tableau is fine, can SQL- relational databases Big part of the job is understanding the systems (claims, policy systems, etc). This person will be reviewing how is the data structured, how is the data formed. The information will be at the Claimant level information will be provided and they should be able to digest. Most of the are relational databases. Need to know how to merge data, understand the data that are capturing and how it relates to similar data, and also mapping out data They current use 7 Insurance systems, for example: Openco, Openbox, MFX, custom built database tools, a lot of them can be home grown etc. Person will most likely be using new system and needs to have the ability to learn that system. More of a data management and reporting role IT is the one actual building the dashboards etc Job Duties: • Provide reporting and data analysis support for various business partners within North American Specialty. • Support data visualization and dashboard efforts across subject areas within the Insurance domain (Submission, Policy/Premium or Claim level analysis). • Ability to learn complex data sources and merge data across disparate systems to meet business requirements. • Ability to work directly with business users to understand requirements and provide recommendations on how best to display data in a report or visual dashboard. • Must have the ability to bridge the communication gap between business users and technical support resources. • Create standard operating procedures for new requirements and manage the transition to offshore support teams or junior staff. • Process change requests on steady state reports with attention to reconciliation expectations. • Automate existing manual reports using database and reporting tool functionality. • Execute standard testing and reconciliation for new or revised standard reports. • Share knowledge with other junior team members. Skills: • SQL expertise required. Requires advanced understanding of data modeling, table relationships, and query optimization. • Ability to own report development effort with minimal supervision. • Problem solving; data related trouble-shooting such as identifying reconciliation variances, or determining cause of data anomalies. • Ability to interview users and understand requirements. • Expert knowledge of Business Objects, PowerBI, Tableau or similar reporting tool required. • Skilled in merging data from multiple disparate sources. Data warehousing experience important. • Expert in MS Excel and MS Access • VBA knowledge a plus • Be able to prioritize based on due dates and task demands. Experience: • 5+ years insurance data experience. • 5+ years SQL • 5+ years’ experience with data warehousing and/or relational databases • Finance, Actuarial or Planning data experience is a plus. About US Tech Solutions: Your talent, our opportunities - This is the premise behind US Tech Solutions. You have the skill we have the opportunity. As a team, we work passionately for you to get the right career opportunity across industry verticals and functions. For past sixteen years, leading Global Companies and Fortune 500 come to us to get the right talent. Whether you want to work as full-time, contractor or part-time, technical or non-technical our talent consultants will connect with the right career opportunity globally. Connect with our talent team today. USTECH was founded in 2000 by Manoj Agarwal. Today, we are a global firm offering talent solutions to 150 customers including 20% of Fortune 500 across Financial Services, Healthcare, Life Sciences, Aerospace, Energy, Retail, Telecom, Technology, Manufacturing, and Engineering. We are headquartered in New Jersey with 40 global locations across the USA, Canada, Europe, and India. Deloitte has recognized USTECH as one of the fastest growing private businesses for the past five consecutive years and INC 500 for the past three. We have also been rated “The Top Business in the US" by Diversity Business since 2011. To learn more about how US Tech Solutions visit our website: www.ustechsolutions.com. “US Tech is an Equal Opportunity Employer" and “US Citizens & all other parties authorized to work in the US are encouraged to apply." Apply: Interested candidates are requested to send their resume to Gurudeep at Gurudeep@ustechsolutionsinc.com""",
    }
    with open(path.join(DIR, "html_files/job.html"), "r") as f:
        job = Job(f.read()).to_dict()

    for field in expected_details:
        assert expected_details[field] == job["details"][field]


def test_handles_full_html_page():
    """Ensure the full html page and the #profile-wrapper element
    given to the Profile constructor yield the same Profile object"""
    with open(path.join(DIR, "html_files/profile.html"), "r") as f:
        profile_html = f.read()
    profile = Profile(profile_html)
    assert profile.personal_info["name"] == "Courtney Ferguson Lee"


def test_image_url():
    """
    Ensure imageURL parsing works on both YOUR profile, and the profiles of
    others. (They have different styling)
    """
    with open(path.join(DIR, "html_files/profile.html"), "r") as f:
        my_profile_html = f.read()
    with open(path.join(DIR, "html_files/otherProfile.html"), "r") as f:
        other_profile_html = f.read()
    my_info = Profile(my_profile_html).to_dict()
    other_info = Profile(other_profile_html).to_dict()
    assert my_info["personal_info"]["image"] and other_info["personal_info"]["image"]
    assert my_info["experiences"]["jobs"][0]["li_company_url"]


if __name__ == "__main__":
    test_company_overview()
    test_handles_full_html_page()
    test_image_url()
