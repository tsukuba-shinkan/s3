# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pickle
import MeCab


# %%
def load_file(name):
    with open("wordtable/"+name+".pickle", "rb") as f:
        return pickle.load(f)


# %%
word_table = load_file("word_table")
page_title_id_table = load_file("page_title_id_table")
page_heading_id_table = load_file("page_heading_id_table")
page_desc_id_table = load_file("page_desc_id_table")
zenbun_table = load_file("zenbun_table")


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
def zenbun_search(result,keyword, score):
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
            set_score(result,word_id, page_title_id_table, 30)
            set_score(result,word_id, page_heading_id_table, 10)
            set_score(result,word_id, page_desc_id_table, 1)
        zenbun_search(result, keyword, 1)
    return result


# %%
page_dict = {}
with open("pages.pickle", "rb") as f:
    for page in pickle.load(f):
        page_dict[page["id"]] = page


# %%
def sort_score(scores):
    score_array = []
    for page_id, score in scores.items():
        score_array.append({
            "page_id": page_id,
            "score": score
        })
    score_array.sort(key=lambda x: x["score"])
    return score_array


# %%
def search(keyword):
    if len(keyword) == 0:
        return
    scores = scored_search(keyword)
    scores = [page_dict[s["page_id"]] for s in sort_score(scores)]
    return scores
    


# %%
search("テスト")


# %%



