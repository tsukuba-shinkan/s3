# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pickle
from bs4 import BeautifulSoup
import MeCab


# %%
word_table = {}  # word(string) -> word_id(int)
word_count = 0
page_title_id_table = {}  # word_id in title(int) -> set of page_id(set<int>)
# word_id in heading(int) -> set of page_id(set<int>)
page_heading_id_table = {}
# word_id in description(int) -> set of page_id(set<int>)
page_desc_id_table = {}
zenbun_table = {}


# %%
def get_word_id(word):
    global word_table
    global word_count
    word = word.lower()
    if word in word_table:
        return word_table[word]
    word_table[word] = word_count
    word_count += 1
    return word_count - 1


# %%
wakati = MeCab.Tagger("-Owakati")
remove_words = {"(", ")", "（", "）", "[", "]",
                "「", "」", "+", "-", "*", "$",
                "'", '"', "、", ".", "”", "’",
                ":", ";", "_", "/", "?", "!",
                "。", ",", "=", "＝"}


class Text():
    def __init__(self, text):
        self.raw = text
        self.wakati = [get_word_id(r) for r in wakati.parse(
            text).split() if r not in remove_words]

    def __repr__(self):
        return str(self.wakati)

    def insert_to_table(self, table, page_id):
        for word_id in self.wakati:
            if word_id not in table:
                table[word_id] = set()
            table[word_id].add(page_id)
        return self


# %%
pages = []
with open("pages.pickle", "rb") as f:
    pages = pickle.load(f)
len(pages)


# %%
def get_event_id(page_id, event_index):
    return page_id*1919 + event_index


# %%
def parse_page(page):
    page_id = page["id"]
    if "title" not in page["event"]:
        return
    for i in range(len(page["event"]["title"])):
        zenbun = ""
        event_id = get_event_id(page_id, i)
        title = Text(page["event"]["title"][i])
        title.insert_to_table(page_title_id_table, event_id)
        zenbun += title.raw

        descHtml = BeautifulSoup(
            page["event"]["description"][i], "html.parser")
        descHeadings = [Text(h.get_text()).insert_to_table(
            page_heading_id_table, event_id) for h in descHtml.select("h1,h2,h3,h4,h5,h6")]
        zenbun += "".join([h.raw for h in descHeadings])

        descText = Text(descHtml.get_text())
        descText.insert_to_table(page_desc_id_table, event_id)
        zenbun = descText.raw

        zenbun_table[event_id] = zenbun.lower()


# %%
for page in pages:
    parse_page(page)


# %%
def write_json(path, data):
    with open("wordtable_event/" + path + ".pickle", "wb") as f:
        pickle.dump(data, f)


# %%
write_json("word_table", {"data": word_table, "count": word_count})
write_json("page_title_id_table", page_title_id_table)
write_json("page_heading_id_table", page_heading_id_table)
write_json("page_desc_id_table", page_desc_id_table)
write_json("zenbun_table", zenbun_table)


# %%
