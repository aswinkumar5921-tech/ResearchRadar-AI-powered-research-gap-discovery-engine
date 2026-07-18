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

        title = paper.get("title", "")

        abstract = reconstruct_abstract(
            paper.get("abstract_inverted_index")
        )

        year = paper.get("publication_year")

        doi = paper.get("doi")

        citations = paper.get("cited_by_count", 0)

        language = paper.get("language")

        paper_type = paper.get("type")

        venue = ""

        primary_location = paper.get("primary_location")

        if primary_location:
            source = primary_location.get("source")

            if source:
                venue = source.get("display_name", "")
                cursor.execute("""
                INSERT OR IGNORE INTO papers
                (openalex_id,
                title,
                abstract,
                publication_year,
                doi,
                cited_by_count,
                language,
                paper_type,
                venue)

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    paper["id"],
                    title,
                    abstract,
                    year,
                    doi,
                    citations,
                    language,
                    paper_type,
                    venue
                ))
conn.commit()
conn.close()

print("Finished importing papers!")