from bs4 import BeautifulSoup
from requests import get
import time
import datetime
import pandas as pd

def grab_job_data(divs):
    allJobsInfo = []
    hitEnd = False
    for div in divs:
        job_id = div.get("data-job-id")
        job_title = div.get("aria-label")
        jobInfo = {
            "jobTitle": job_title if job_title else None,
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
        if var and "d" in var.get_text():
            hitEnd = True
            return{
                "jobsList": allJobsInfo,
                "hitEnd": True
            }
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

    return {
        "jobsList": allJobsInfo,
        "hitEnd": hitEnd
    }

def searchJobs(link_):
    returnArray = []
    loopFlag = True
    pageCounter = 1
    while loopFlag:
        link1 = link_ + "?page=" + str(pageCounter)
        print("Searching page " + link1 + "..." + "\n")
        response = get(link1, headers={"User-Agent": "Mozilla/5.0"})
        html_soup = BeautifulSoup(response.text, "html.parser")
        jInfo = grab_job_data(html_soup.find_all("article", {"data-automation": "jobDetailsPage"}))
        for j in jInfo["jobsList"]:
            returnArray.append(j)

        if jInfo["hitEnd"] == True:
            break
        pageCounter += 1
        time.sleep(1)  # To avoid hitting the server too fast
    return returnArray

region = input("REGION\nRegions must be entered with a '-'symbol between each word (but not before or after) E.g: 'All-Brisbane'\nEnter a region: ")
print()
category = input("CATEGORY\nCategories must be entered with a '-'symbol between each word (but not before or after) E.g: 'information-technology'\nEnter a category: ")
print()

link = "https://www.seek.com.au/" + category + "-jobs/in-" + region
print("Searching for jobs in " + link + "...\n")
jobs = searchJobs(link)
print("Found " + str(len(jobs)) + " jobs in total.\n")

df = pd.DataFrame(jobs)
if not df.empty:
    df.to_csv("jobs_" + region + "_" + category + ".csv", index=False)
    print("Data saved to 'jobs_" + region + "_" + category + ".csv'.")