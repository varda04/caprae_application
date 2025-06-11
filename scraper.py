# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import quote
from validate_email import validate_email
from googlesearch import search
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

def scrape_naukri_jobs(keyword, location, max_pages):
    jobs = []
    seen= set()
    k_dash = keyword.replace(" ", "-")
    l_dash = location.replace(" ", "-")
    k_enc = quote(keyword)
    l_enc = quote(location)

    # Setup Selenium Chrome options (headless mode)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    )

    # Updated path to your ChromeDriver executable
    service = Service(r"C:\Users\varda\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    
    try:
        for i in range(0,max_pages):
            url = (
                f"https://www.naukri.com/{k_dash}-jobs-in-{l_dash}"
                # f"?k={k_enc}&l={l_enc}"
                f"-{i}"
            )
            print("Fetching:", url)
            driver.get(url)

            # Wait for the job cards container to be loaded (adjust selector if needed)
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.srp-jobtuple-wrapper")))

            # Get page source after JS execution
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # find each job wrapper
            cards = soup.find_all("div", class_="srp-jobtuple-wrapper")

            for card in cards:
                # title & link
                a_title = card.find("a", class_="title")
                title = a_title.get_text(strip=True) if a_title else None
                link = a_title["href"] if a_title and a_title.has_attr("href") else None

                # company
                a_comp = card.find("a", class_="comp-name")
                company = a_comp.get_text(strip=True) if a_comp else None

                # experience
                exp = card.find("span", class_="expwdth")
                experience = exp.get_text(strip=True) if exp else None

                # location
                loc = card.find("span", class_="locWdth")
                location_text = loc.get_text(strip=True) if loc else None

                # description snippet
                desc = card.find("span", class_="job-desc")
                description = desc.get_text(strip=True) if desc else None

                # tags
                tags = [li.get_text(strip=True) for li in card.select("ul.tags-gt li")]

                # posted date / age
                posted = card.find("span", class_="job-post-day")
                posted_text = posted.get_text(strip=True) if posted else None

                unique_key = (title, company, location_text)
                if unique_key in seen:
                    continue
                seen.add(unique_key)

                job_data = {
                    "title": title,
                    "link": link,
                    "company": company,
                    "experience": experience,
                    "location": location_text,
                    "description": description,
                    "tags": tags,
                    "posted": posted_text,
                }
                jobs.append(job_data)
                print(job_data)

    finally:
        driver.quit()

    return jobs

from duckduckgo_search import DDGS

import requests
from bs4 import BeautifulSoup

from duckduckgo_search import DDGS

from duckduckgo_search import DDGS

def get_company_website(company, location):
    query = f"{company} {location} official website"
    print(f"[Google Search] Querying: {query}")
    
    try:
        for i, url in enumerate(search(query, num_results=5)):
            print(f"[Google Result {i}] URL: {url}")
            if company.lower().split()[0] in url.lower():
                print(f"[Google Result {i}] Match found: {url}")
                return url
        print("[Google Search] No matching result found.")
    except Exception as e:
        print("[Google Search] Error:", e)

    return None



def scrape_contact_info(domain):
    guessed = generate_valid_email(domain)
    return {"email": guessed if guessed else "Not found"}
    
def generate_valid_email(domain):
    domain = domain.strip().lower()
    domain = re.sub(r'^https?://', '', domain).split('/')[0]
    domain= re.sub(r'^www.', '', domain)
    print("Cleaned domain:", domain)
    if "linkedin.com" in domain:
        return "LinkedIn page, no contact info"

    prefixes = [
        "hr", "careers", "jobs", "admin", "info"
    ]

    print("Finding valid email for", domain)
    for prefix in prefixes:
        guess = f"{prefix}@{domain}"
        if validate_email(
            guess,
            smtp_timeout=2
            ):
            print("Valid guessed email:", guess)
            return guess 
    return None