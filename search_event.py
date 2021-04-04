# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pickle
import MeCab
import time
from datetime import datetime


# %%
def load_file(name):
    with open("wordtable_event/"+name+".pickle", "rb") as f:
        return pickle.load(f)


# %%
word_table = load_file("word_table")
page_title_id_table = load_file("page_title_id_table")
page_heading_id_table = load_file("page_heading_id_table")
page_desc_id_table = load_file("page_desc_id_table")
zenbun_table = load_file("zenbun_table")
event_dict = {}


# %%
def load_tables():
    global page_title_id_table
    global page_desc_id_table
    global page_heading_id_table
    global zenbun_table
    global word_table

    word_table = load_file("word_table")
    page_title_id_table = load_file("page_title_id_table")
    page_heading_id_table = load_file("page_heading_id_table")
    page_desc_id_table = load_file("page_desc_id_table")
    zenbun_table = load_file("zenbun_table")

    global event_dict
    with open("pages.pickle", "rb") as f:
        for page in pickle.load(f):
            page_id = page["id"]
            if "title" not in page["event"]:
                continue
            for i in range(len(page["event"]["title"])):
                event_id = get_event_id(page_id, i)
                event_dict[event_id] = {
                    "title": page["event"]["title"][i],
                    "start": page["event"]["start"][i],
                    "end": page["event"]["end"][i],
                    "page_id": page_id,
                    "description": page["event"]["description"][i],
                    "page": page
                }


# %%
def get_word_id(word):
    global word_table
    if word not in word_table["data"]:
        return None
    return word_table["data"][word]


# %%
wakati = MeCab.Tagger("-Owakati")
remove_words = {"(", ")", "（", "）", "[", "]",
                "「", "」", "+", "-", "*", "$",
                "'", '"', "、", ".", "”", "’",
                ":", ";", "_", "/", "?", "!",
                "。", ",", "=", "＝"}


def split_word(keyword):
    return [get_word_id(r) for r in wakati.parse(keyword).split() if r not in remove_words]


# %%
def set_score(result, word_id, table, score):
    if word_id not in table:
        return
    pageset = table[word_id]
    for page in pageset:
        if page not in result:
            result[page] = 0
        result[page] += score


def zenbun_search(result, keyword, score):
    global zenbun_table
    for page_id, zenbun in zenbun_table.items():
        if keyword in zenbun:
            if page_id not in result:
                result[page_id] = 0
            result[page_id] += score


# %%
def scored_search(keyword):
    result = {}
    for word_id in split_word(keyword):
        if word_id is not None:
            set_score(result, word_id, page_title_id_table, 30)
            set_score(result, word_id, page_heading_id_table, 10)
            set_score(result, word_id, page_desc_id_table, 1)
        zenbun_search(result, keyword, 1)
    return result


# %%
def get_event_id(page_id, event_index):
    return page_id*1919 + event_index


# %%
def sort_score(scores):
    score_array = []
    for page_id, score in scores.items():
        score_array.append({
            "event_id": page_id,
            "score": score
        })
    score_array.sort(key=lambda x: x["score"], reverse=True)
    return score_array


# %%
currenttime = 0


def reload():
    global currenttime
    if time.time() - currenttime < 5:
        return
    load_tables()
    currenttime = time.time()


# %%
def keyword_search(keyword):
    if len(keyword) == 0:
        return
    reload()
    scores = scored_search(keyword)
    scores = [event_dict[s["event_id"]] for s in sort_score(scores)]
    return scores


# %%
def filter_by_date(events, a, b):
    # pass if a<start<b or a<end<b
    a = datetime.fromisoformat(a)
    b = datetime.fromisoformat(b)
    result = []
    for e in events:
        try:
            start = datetime.fromisoformat(e["start"])
            end = datetime.fromisoformat(e["end"])
            if a < start < b or a < end < b:
                result.append(e)
        except:
            continue
    return result


# %%
def get_all():
    global event_dict
    return [i for i in event_dict.values()]


# %%
def search(keyword="", rangestart="2021-04-01", rangeend="2021-12-31"):
    events = []
    if len(keyword) == 0:
        reload()
        events = get_all()
    else:
        events = keyword_search(keyword)
    return(filter_by_date(events, rangestart, rangeend))
