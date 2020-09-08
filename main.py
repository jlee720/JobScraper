import csv
from indeed_jobs import get_indeed_jobs

def find_new_grad_jobs():
  return get_indeed_jobs()

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Location", "Link"])

  for i in range(len(jobs)):
    writer.writerow(list(jobs[i].values()))

  return None

save_to_file(find_new_grad_jobs())