import requests
import sqlite3
import time

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

url = "https://api.openalex.org/works"

cursor_value = "*"

while True:

    params = {
        "search": "large language models",
        "per-page": 200,
        "cursor": cursor_value
    }

    response = requests.get(url, params=params)
    data = response.json()

    papers = data["results"]

    if len(papers) == 0:
        break

    for paper in papers:

        cursor.execute("""
        INSERT OR IGNORE INTO papers
        (openalex_id, title, year, citations)
        VALUES (?, ?, ?, ?)
        """, (
            paper["id"],
            paper["title"],
            paper["publication_year"],
            paper["cited_by_count"]
        ))

    conn.commit()

    print(f"Downloaded {len(papers)} papers")

    cursor_value = data["meta"]["next_cursor"]

    time.sleep(1)

conn.close()

print("Finished!")