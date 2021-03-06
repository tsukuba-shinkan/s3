# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests as rq
import csv
import pickle
import os
import time


# %%
s = rq.Session()


# %%
def wpFetch(url):
    url = "https://www.stb.tsukuba.ac.jp/~shinkan-web/orgadmin/?rest_route=/wp" + url
    return s.get(url).json()


# %%
q = s.post("https://www.stb.tsukuba.ac.jp/~shinkan-web/orgadmin/wp-login.php",
           data={"log": os.environ["CRAWLER_USERID"],
                 "pwd": os.environ["CRAWLER_PASSWORD"], "testcookie": "0"},
           headers={'user-agent': 'FireFox'}
           )


# %%
pages = wpFetch("/v2/pages&status=draft,publish&per_page=100&page=1") + wpFetch(
    "/v2/pages&status=draft,publish&per_page=100&page=2") + wpFetch("/v2/pages&status=draft,publish&per_page=100&page=3")


# %%
len(pages)


# %%
with open("pages.pickle", "wb") as f:
    pickle.dump({"data": pages, "timestamp": time.time()}, f)
