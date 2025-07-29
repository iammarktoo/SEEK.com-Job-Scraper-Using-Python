from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta



options = Options()
options.add_argument("--window-size = 1920,1080")

driver = webdriver.Chrome(options=options)
#Form SEEK search URLs
region = input("REGION\nRegions must be entered with a '-' symbol between each word (but not before or after) E.g: 'All-Brisbane'\nEnter a region: ")
category = input("CATEGORY\nCategories must be entered with a '-' symbol between each word (but not before or after) E.g: 'information-technology'\nEnter a category: ")

while True:
    date_range = input("DATE RANGE\nPlease enter your search date range (choices: 1 / 3 / 7 / 14 / 30): ")
    valid_inputs = ["1", "3", "7", "14", "30"]
    if date_range in valid_inputs:
        break
    else:
        print("Invalid date range. Please try again.\n")

base_url = "https://www.seek.com.au/" + category + "-jobs/in-"+region+"?daterange="+date_range
page = 1
job_ids = []

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

