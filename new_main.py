from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


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

#Scrape job info form URLs
for id in job_ids:
    job_url = "https://www.seek.com.au/job/"+id+"&ref=search-standalone"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-automation="jobAdDetails"]'))
        )
    except:
        print("Page failed to load properly.")
        break

    div = BeautifulSoup(driver.page_source, "html.parser")
    jobInfo = {
            "jobTitle": None,
            "companyName": None,
            "location": None,
            "pay": None,
            "category": None,
            "description": "",
            "featured": div.get("data-automation") == "premiumJob",
            "postedDate": str(datetime.date.today()),
            "jobURL": "https://www.seek.com.au/" + category + "-jobs/in-" + region + "?jobId=" + job_id if job_id else None,
        }
    var = div.find("span", {"data-automation": "jobListingDate"})
    
    var = div.find("a", {"data-automation": "jobTitle"})
    if (var == None): jobInfo["jobTitle"] = None
    else: jobInfo["jobTitle"] = var.get_text()

    var = div.find("a", {"data-automation": "jobCompany"})
    if (var == None): jobInfo["companyName"] = None
    else: jobInfo["companyName"] = var.get_text()

    var = div.find("a", {"data-automation": "jobLocation"})
    if (var == None): jobInfo["location"] = None    
    else: jobInfo["location"] = var.get_text()

    var = div.find("a", {"data-automation": "jobSalary"})
    if (var == None): jobInfo["pay"] = None 
    else: jobInfo["pay"] = var.get_text()

    var = div.find("a", {"data-automation": "jobClassification"})
    if (var == None): jobInfo["category"] = None
    else: jobInfo["category"] = var.get_text()

    var = div.find("a", {"data-automation": "jobDetails"})
    if (var == None): jobInfo["description1"] = None
    else: jobInfo["description"] = var.get_text()

    var = div.find("article", {"data-automation": "premiumJob"})
    if (var == None): jobInfo["featured"] = False
    else: jobInfo["featured"] = True

    var = div.find("a", {"data-automation": "jobTitle"})
    if (var == None): jobInfo["jobURL"] = None
    else: jobInfo["jobURL"] = div.find("a", {"data-automation": "jobTitle"})['href']

    allJobsInfo.append(jobInfo)



