import sqlite3
import numpy as np
from fastembed import TextEmbedding

model = TextEmbedding()

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id,title,abstract
FROM papers
""")

papers = cursor.fetchall()

print(f"Found {len(papers)} papers")

embeddings = {}

for paper_id, title, abstract in papers:

    text = f"{title}\n\n{abstract}"

    vector = list(model.embed([text]))[0]

    embeddings[paper_id] = np.array(vector)

print("Embeddings generated:", len(embeddings))