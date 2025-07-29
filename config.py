#URL builder
BASE_URL = "https://www.seek.com.au"
REGION = input("REGION\nRegions must be entered with a '-' symbol between each word (but not before or after) E.g: 'All-Brisbane'\nEnter a region: ")
CATEGORY = input("CATEGORY\nCategories must be entered with a '-' symbol between each word (but not before or after) E.g: 'information-technology'\nEnter a category: ")

while True:
    DATE_RANGE = input("DATE RANGE\nPlease enter your search date range (choices: 1 / 3 / 7 / 14 / 30): ")
    valid_inputs = ["1", "3", "7", "14", "30"]
    if DATE_RANGE in valid_inputs:
        break
    else:
        print("Invalid date range. Please try again.\n")

#Selenium settings
WINDOW_SIZE = "1920,1080"
HEADLESS = False
SELENIUM_TIMEOUT = 10

#Output config
SAVE_TO_CSV = True
CSV_FILENAME = "seek_jobs.csv"