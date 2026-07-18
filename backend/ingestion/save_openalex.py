import requests
import sqlite3

# Connect to database
conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

# OpenAlex API
url = "https://api.openalex.org/works"

params = {
    "search": "large language models",
    "per-page": 5
}

response = requests.get(url, params=params)
data = response.json()

# Save papers
for paper in data["results"]:

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
conn.close()

print("Papers saved successfully!")