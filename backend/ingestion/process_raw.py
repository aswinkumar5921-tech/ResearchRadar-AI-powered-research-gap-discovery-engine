import os
import json
import sqlite3

conn=sqlite3.connect("data/sqlite/research.db")
cursor=conn.cursor()

def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return ""

    words = []

    for word, positions in inverted_index.items():
        for pos in positions:
            words.append((pos, word))

    words.sort()

    return " ".join(word for pos, word in words)

files = sorted(os.listdir("data/raw"))
for file in files:

    with open(f"data/raw/{file}", "r", encoding="utf-8") as f:
        data = json.load(f)

    for paper in data["results"]:
        print(paper["title"])