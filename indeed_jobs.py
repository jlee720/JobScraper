
import requests
from bs4 import BeautifulSoup

JOBS_KEYWORD = {
  "NEW_GRAD" : "new+graduate+software+engineer"
}

LIMIT = 50
URL = f"https://ca.indeed.com/jobs?q={JOBS_KEYWORD['NEW_GRAD']}&l=Canada"

def extract_indeed_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')

  pagination = soup.find("div", {"class": "pagination"})

  list_links = pagination.find("ul").find_all('a')
  list_pages = []

  for i in range(len(list_links) - 1):
    page_num = int(list_links[i].find("span").string)
    list_pages.append(page_num)

  last_page = list_pages[-1]

  return last_page

def extract_job_data(job_html):
    title = job_html.find("h2", {"class": "title"}).find("a")["title"]
    company = job_html.find("div", {"class": "sjcl"}).find("span", {"class": "company"})

    if company.find("a") is not None:
      company = str(company.find("a").string).strip()
    else:
      company = str(company.string).strip()

    location = job_html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = job_html["data-jk"]

    return {
      'title': title,
      'company': company,
      'location': location,
      'link': f"https://ca.indeed.com/viewjob?jk={job_id}"
    }

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get((f"{URL}&limit={page * LIMIT}"))
    soup = BeautifulSoup(result.text, 'html.parser')
    job_results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    
    for j in range(len(job_results)):
      data = extract_job_data(job_results[j])
      jobs.append(data)

  return jobs

def get_indeed_jobs():
  last_indeed_page = extract_indeed_pages()
  indeed_jobs = extract_indeed_jobs(last_indeed_page)

  return indeed_jobs