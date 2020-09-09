import csv
from flask import Flask, render_template, request, redirect, send_file
from indeed_scrapper import get_indeed_jobs

app = Flask("Job Scraper")
db = {}

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Location", "Link"])

  print("Writing...")
  for i in range(len(jobs)):
    writer.writerow(list(jobs[i].values()))
  print("Successfully finished saving a file")

  return

def fetch_from_cache(keyword):
  fromDb = db.get(keyword)
  if fromDb is not None:
    return fromDb
  else:
    return None

@app.route("/")
def home():
  return render_template("main_page.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word is not None:
    word = word.lower()
    jobs = fetch_from_cache(word)
    if jobs is None:
      jobs = get_indeed_jobs(word)
      db[word] = jobs
    return render_template("report.html",
      search=word,
      resultsLen=len(jobs),
      jobs=jobs
    )
  else:
    return redirect("/")

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if word is not None:
      word = word.lower()
      jobs = fetch_from_cache(word)
      if jobs is None:
        raise Exception()
      save_to_file(jobs)
      return send_file("jobs.csv", as_attachment=True)
    else:
      raise Exception()

  except:
    return redirect("/")

app.run(host="0.0.0.0")