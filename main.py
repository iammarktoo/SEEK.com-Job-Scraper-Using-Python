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
base_url = f'https://www.seek.co.au/jobs-in-{category}/in-{region}?page={page}'

#Grab the user's windows username
username = os.getlogin()

#Name the output file
file_name = f'seek_{region}_{category}_{keyword}.csv'
save_path = f'C:/Users/{username}/Desktop/'
complete_path = os.path.join(save_path, file_name)

#Create CSV file
csv_file = open(complete_path, 'w+', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title', 'Company', 'Type', 'Location', 'Salary', 'Field', 'Bulletpoints', 'Description'])

#Main Scrape Function
def grab_job_data():
    job = req.html.find('._1wkzzau0.a1msqi7e')
    
    for jobs in job:
        job_title = jobs.find('._1wkzzau0._1wkzzauf._1rct8jy4._1rct8jy6._1rct8jy9.lnocuo2._1rct8jya._1rct8jyd._1wkzzau0._1wkzzauf.a1msqih', first = True).text
        job_company = jobs.find('._1wkzzau0._1wkzzauf._842p0a0', first=True).text
        
        try:
            job_type = jobs.find('._1wkzzau0.a1msqi5i.a1msqi0._6ly8y50', containing='time', first=True).text
        except Exception as e:
            job_type = 'Could not find job type'
        job_location = jobs.find('div._1wkzzau0.a1msqi6q > span._1wkzzau0.a1msqi4y.lnocuo0.lnocuo1.lnocuo21._1d0g9qk4.lnocuo7', first=True).text
        
        try:
            job_salary_info = jobs.find('._1wkzzau0.v28kuf0.v28kuf4.v28kuf2', first=True).text
        except Exception as e:
            job_salary_info = 'Could not find salary information'
            
        job_field = jobs.find('div._1wkzzau0.a1msqi6q.a1msqi4u.a1msqi4z > span._1wkzzau0.a1msqi4y.lnocuo0.lnocuo1.lnocuo21._1d0g9qk4.lnocuo7 > div._1wkzzau0.szurmz0.szurmzb > div._1wkzzau0.a1msqigi.a1msqi5a.a1msqig2.szurmz2j > div._1wkzzau0.a1msqir.a1msqif6.a1msqibu.a1msqi4y.a1msqifm > a._1wkzzau0._1wkzzauf._842p0a0', first=True).text
        
        try:
            job_bulletpoints = jobs.find('ul._1wkzzau0._1wkzzau3.szurmz0.szurmz4', first=True).text
        except Exception as e:
            job_bulletpoints = 'Could not find bullet points'

        job_description = jobs.find('span._1wkzzau0.a1msqi4y.lnocuo0.lnocuo1.lnocuo22._1d0g9qk4.lnocuo7', first=True).text
        
        print(f'Title: {job_title}')
        print(f'Company: {job_company}')    
        print(f'Type: {job_type}')
        print(f'Location: {job_location}')
        print(f'Salary: {job_salary_info}')
        print(f'Field: {job_field}')
        print(f'Bulletpoints: {job_bulletpoints}')
        print(f'Description: {job_description}')
        print('----------------------------------------')   
        csv_writer.writerow([job_title, job_company, job_type, job_location, job_salary_info, job_field, job_bulletpoints, job_description])
        
#Loop through the pages
for n in range(1, pages_to_scrape + 1):
    page = str(n)
    base_url = f"https://www.seek.co.au/jobs-in-{category}/in-{region}?page={page}"
    req = session.get(base_url)
    req.html.render(sleep=1, timeout=20)
    print(f'Scraping page {page}...')
    grab_job_data()
#Close the CSV file
csv_file.close()