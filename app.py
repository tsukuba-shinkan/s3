from fastapi import FastAPI
import search
import search_event
import subprocess
app = FastAPI()


@app.get("/search/org")
def searchOrgs(q: str):
  if len(q) == 0:
    return []
  return search.search(q)


@app.get("/search/events")
def searchEvents(q: str):
  if len(q) == 0:
    return []
  return search_event.search(q)
