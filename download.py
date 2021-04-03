# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests as rq
import csv
import pickle


# %%
s = rq.Session()


# %%
def wpFetch(url):
    url = "https://www.stb.tsukuba.ac.jp/~shinkan-web/orgadmin/?rest_route=/wp" + url
    return s.get(url).json()


# %%
q = s.post("https://www.stb.tsukuba.ac.jp/~shinkan-web/orgadmin/wp-login.php", 
          data={"log": "github_crawler", "pwd": "v$ge)M%nbZ^buACHJQfj#FSJ", "testcookie": "0"},
         headers = {'user-agent': 'FireFox'}
)


# %%
pages = wpFetch("/v2/pages&status=draft,publish&per_page=100&page=1") + wpFetch("/v2/pages&status=draft,publish&per_page=100&page=2") + wpFetch("/v2/pages&status=draft,publish&per_page=100&page=3")


# %%
len(pages)


# %%
with open("pages.pickle", "wb") as f:
    pickle.dump(pages, f)


