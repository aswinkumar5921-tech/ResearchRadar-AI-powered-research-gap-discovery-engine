import sqlite3
import numpy as np
from fastembed import TextEmbedding

print("Loading embedding model...")
model = TextEmbedding()
print("Model loaded!")

# -------------------------
# Load Papers
# -------------------------
conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, title, abstract
FROM papers
""")

papers = cursor.fetchall()

print(f"Loaded {len(papers)} papers")

embeddings = []

for paper_id, title, abstract in papers:

    text = f"{title}\n\n{abstract or ''}"

    vector = list(model.embed([text]))[0]

    embeddings.append(
        (
            paper_id,
            np.array(vector)
        )
    )

print(f"\nGenerated {len(embeddings)} embeddings")

print("Embedding shape:", embeddings[0][1].shape)

import os

os.makedirs("data/embeddings", exist_ok=True)

ids = np.array([x[0] for x in embeddings])

vectors = np.vstack([x[1] for x in embeddings])

np.save("data/embeddings/paper_ids.npy", ids)
np.save("data/embeddings/paper_vectors.npy", vectors)

print("Embeddings saved successfully!")

conn.close()