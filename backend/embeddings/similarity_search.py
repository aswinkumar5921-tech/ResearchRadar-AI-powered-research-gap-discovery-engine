import sqlite3
import numpy as np
from fastembed import TextEmbedding
from sklearn.metrics.pairwise import cosine_similarity

print("Loading model...")
model = TextEmbedding()

print("Loading embeddings...")
paper_ids = np.load("data/embeddings/paper_ids.npy")
paper_vectors = np.load("data/embeddings/paper_vectors.npy")

query = input("\nEnter your research topic: ")

query_vector = list(model.embed([query]))[0]
query_vector = np.array(query_vector).reshape(1, -1)

similarities = cosine_similarity(query_vector, paper_vectors)[0]

top_indices = np.argsort(similarities)[::-1][:10]

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

print("\nTop 10 Similar Papers\n")

for rank, idx in enumerate(top_indices, start=1):

    paper_id = int(paper_ids[idx])

    cursor.execute(
        "SELECT title, publication_year FROM papers WHERE id=?",
        (paper_id,)
    )

    result = cursor.fetchone()

    if result:
        title, year = result

        print(f"{rank}. {title}")
        print(f"   Year: {year}")
        print(f"   Similarity: {similarities[idx]:.4f}\n")

conn.close()