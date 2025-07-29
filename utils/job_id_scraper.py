from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

from config import BASE_URL, CATEGORY, REGION, DATE_RANGE, SELENIUM_TIMEOUT
from selenium_setup import create_driver


def get_job_ids():
    driver = create_driver()
    job_ids = []
    page = 1
    base_url = f"{BASE_URL}/{CATEGORY}-jobs/in-{REGION}?daterange={DATE_RANGE}"
    
    while True:
        url = base_url + f"&page={page}"
        print(f"Scraping page {page}: {url}")
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="job-card"]'))
            )
        except:
            print("Page failed to load properly.")
            break

        soup = BeautifulSoup(driver.page_source, "html.parser")

        #Find all job cards
        job_cards = soup.find_all("article", {"data-testid": "job-card"})
        print(f"Found {len(job_cards)} job cards.\n")

        #Extract job IDs
        for card in job_cards:
            id = card.get("data-job-id")
            if id:
                job_ids.append(id)
        #Check for "Next" button
        next_btn = soup.find("a", attrs={"aria-label": "Next", "data-automation": True})
        if next_btn:
            page += 1
            time.sleep(2)
        else:
            break
    driver.quit()
    return job_ids

