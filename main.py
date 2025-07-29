from utils.job_info_scraper import scrape_info
from utils.job_id_scraper import get_job_ids
from concurrent.futures import ThreadPoolExecutor, as_completed

job_ids = get_job_ids
all_jobs_info = []

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(scrape_info, job_id): job_id for job_id in job_ids}
    for future in as_completed(futures):
        result = future.result()
        all_jobs_info.append(result)

print(f"\nScraped {len(all_jobs_info)} job listings")
