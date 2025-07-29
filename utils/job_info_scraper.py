from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import re


#Function to scrape a single job ID
def scrape_info(id):
    allJobsInfo = []
    driver = create_driver()
    job_url = "https://www.seek.com.au/job/"+str(id)+"&ref=search-standalone"
    job_info = {
        "jobTitle":None,
            "companyName":None,
            "location":None,
            "pay":None,
            "category":None,
            "postedDate":None,
            "description": "",
            "featured":False,
            "jobURL":job_url,
    }

    try:
        driver.get(job_url)
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-automation="jobAdDetails"]'))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        def extract(selector):
            tag = soup.find(attrs={"data-automation": selector})
            return tag.get_text(strip=True) if tag else None
        job_info["jobTitle"] = extract("job-detail-title")
        job_info["companyName"] = extract("advertiser-name")
        job_info["location"] = extract("job-detail-location")
        job_info["pay"] = extract("job-detail-salary")
        job_info["category"] = extract("job-detail-classfications")

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
        job_info["postedDate"] = str(posted_date)
        #Extract Description
        desc_tag = soup.find("div",{"data-automation":"jobAdDetails"})
        if desc_tag:
            job_info["description"] = desc_tag.get_text(strip=True)

        allJobsInfo.append(job_info)
    except:
        print(f"Error with job ID {id}: {e}")
    finally:
        driver.quit()
    return job_info

    
        


