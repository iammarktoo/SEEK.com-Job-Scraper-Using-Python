from requests_html import HTML, HTMLSession
import csv
import os

session = HTMLSession()

#User Input
region = input("REGION\nRegions must be entered with a '-'symbol between each word (but not before or after) E.g: 'All-Brisbane'\nEnter a region: ")
print()
category = input("CATEGORY\nCategories must be entered with a '-'symbol between each word (but not before or after) E.g: 'information-technology'\nEnter a category: ")
print()
page = '1'
keyword = input("KEYWORD\nKeywords must be entered with a '-'symbol between each word (but not before or after) E.g: 'data-analyst'\nEnter a keyword: ")
print()
pages = input("PAGES\nEnter the number of pages to scrape (default is 1): ")
print()

#Create a base URL and append user inputs
base_url = f'https://www.seek.com.au/{category}-jobs/in-{region}?keywords={keyword}&page={page}'

#Grab the user's windows username
username = os.getlogin()

#Name the output file
