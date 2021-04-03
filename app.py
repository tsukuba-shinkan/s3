from fastapi import FastAPI
import search
import search_event
import subprocess
import pickle
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


origins = [
    "https://stb.tsukuba.ac.jp",
    "https://www.stb.tsukuba.ac.jp",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search/org")
def searchOrgs(q: str):
  if len(q) == 0:
    return []
  return search.search(q)


@app.get("/search/events")
def searchEvents(q: str, rangestart:str="2021-04-01", rangeend:str="2021-12-31"):
  return search_event.search(q,rangestart=rangestart, rangeend=rangeend)

@app.get("/random/org")
def randomOrg(n: int = 15):
  return search.random_org(n)

@app.get("/sync")
def sync():
  subprocess.run(["python3", "download.py"])
  subprocess.run(["python3", "gen_wordtable.py"])
  subprocess.run(["python3", "gen_wordtable_event.py"])
  return {"success": True}

@app.get("/all")
def all():
  with open("pages.pickle", "rb") as f:
    return pickle.load(f)


