# SEEK.com Job Scraper Using Python 

A powerful and modular Python-based web scraper that extracts job listings from [SEEK.com.au](https://www.seek.com.au), one of Australia's leading job boards. It supports multi-page scraping, detailed job info extraction, and parallel processing using `concurrent.futures`.

## Features

- ✅ Scrapes job IDs from search results by region, category, and date range
- 🔎 Fetches detailed job listings including:
  - Job title
  - Company name
  - Location
  - Salary
  - Category
  - Posted date
  - Full job description
- 🚀 Parallel processing for fast scraping
- 🧩 Modular codebase for easy maintenance and extension

## Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/iammarktoo/SEEK.com-Job-Scraper-Using-Python.git
   cd SEEK.com-Job-Scraper-Using-Python

2. **Install dependencies**
    ```bash
      pip install -r requirements.txt
    
## How to Run

1. **From the root directory, execute:**
   ```bash
      python main.py

3. **You’ll be prompted to enter:**

- A region (e.g., All-Brisbane)

- A category (e.g., data-analyst)

- A date range (1 / 3 / 7 / 14 / 30)

3. **The program will:**

- Navigate through all result pages

- Extract job IDs

- Scrape job details concurrently

- Save the scraped data into a .csv file

- You can configure options (e.g., headless mode) in config.py.

