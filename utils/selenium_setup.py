from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import WINDOW_SIZE, HEADLESS

#Chrome driver setting
def create_driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
    options.add_argument(f"--window-size={WINDOW_SIZE}")
    driver = webdriver.Chrome(options=options)
    return driver