from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

options = Options()
options.add_argument("--window-size = 1920,1080")

driver = webdriver.Chrome(options=options)
job_ids = [85758177]
#Scrape job info form URLs
allJobsInfo = []
for id in job_ids:
    job_url = "https://www.seek.com.au/job/"+str(id)+"&ref=search-standalone"
    driver.get(job_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-automation="jobAdDetails"]'))
        )
    except:
        print("Page failed to load properly.")
        break
    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobInfo = {
            "jobTitle": None,
            "companyName": None,
            "location": None,
            "pay": None,
            "category": None,
            "postedDate":None,
            "description": "",
            "featured":  bool(soup.find("article", {"data-automation": "premiumJob"})),
            "jobURL": job_url,
        }
    def extract(selector):
        tag = soup.find(attrs={"data-automation": selector})
        return tag.get_text(strip=True) if tag else None
    
    jobInfo["jobTitle"] = extract("job-detail-title")
    jobInfo["companyName"] = extract("advertiser-name")
    jobInfo["location"] = extract("job-detail-location")
    jobInfo["pay"] = extract("job-detail-salary")
    jobInfo["category"] = extract("job-detail-classfications")

    #Extract the posted time
    posted_tag = soup.find("span", string=lambda text: text and "Posted" in text)
    posted_str = posted_tag.get_text(strip=True) if posted_tag else None
    #Default to today's date if parsing fails
    posted_date = datetime.today().date()

    if posted_str:
        match = re.search(r"Posted\s+(\d+)([hd])", posted_str)
        if match:
            value, unit = int(match.group(1)), match.group(2)
            if unit == "h":
                posted_date = (datetime.now()-timedelta(hours=value)).date()
            elif unit == "d":
                posted_date = (datetime.now()-timedelta(days=value)).date()
    #Save date
    jobInfo["postedDate"] = str(posted_date)



    desc_tag = soup.find("div", {"data-automation": "jobAdDetails"})
    if desc_tag:
        jobInfo["description"] = desc_tag.get_text(strip=True)

    allJobsInfo.append(jobInfo)

print(allJobsInfo)



