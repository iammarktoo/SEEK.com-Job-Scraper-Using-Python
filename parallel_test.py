from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

#Chrome driver setting
def create_driver():
    options = Options()
    options.add_argument("--headless=new") # headless mode for speed
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)
#Function to scrape a single job ID
