
import requests
from bs4 import BeautifulSoup

LIMIT = 50

def extract_indeed_pages(url):
  result = requests.get(url)
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

def extract_indeed_jobs(url, last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get((f"{url}&limit={page * LIMIT}"))
    soup = BeautifulSoup(result.text, 'html.parser')
    job_results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    
    for j in range(len(job_results)):
      data = extract_job_data(job_results[j])
      jobs.append(data)

  return jobs

def get_indeed_jobs(keyword):
  url = f"https://ca.indeed.com/jobs?q={keyword}&l=Canada"
  last_indeed_page = extract_indeed_pages(url)
  indeed_jobs = extract_indeed_jobs(url, last_indeed_page)

  return indeed_jobs