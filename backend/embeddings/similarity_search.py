import sqlite3
import numpy as np
from fastembed import TextEmbedding
from sklearn.metrics.pairwise import cosine_similarity

print("Loading embedding model...")
model = TextEmbedding()

print("Loading embedding vectors...")
paper_ids = np.load("data/embeddings/paper_ids.npy")
paper_vectors = np.load("data/embeddings/paper_vectors.npy")


def search_similar_papers(query, top_k=10):

    query_vector = list(model.embed([query]))[0]
    query_vector = np.array(query_vector).reshape(1, -1)

    similarities = cosine_similarity(
        query_vector,
        paper_vectors
    )[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    conn = sqlite3.connect("data/sqlite/research.db")
    cursor = conn.cursor()

    results = []

    for idx in top_indices:

        paper_id = int(paper_ids[idx])

        cursor.execute(
            """
            SELECT
                title,
                publication_year,
                cited_by_count
            FROM papers
            WHERE id = ?
            """,
            (paper_id,)
        )

        paper = cursor.fetchone()

        if paper:

            title, year, citations = paper

            results.append(
                {
                    "paper_id": paper_id,
                    "title": title,
                    "year": year,
                    "citations": citations or 0,
                    "similarity": float(similarities[idx])
                }
            )

    conn.close()

    return results


if __name__ == "__main__":

    query = input("Enter research topic: ")

    papers = search_similar_papers(query)

    print("\nTop Similar Papers\n")

    for i, paper in enumerate(papers, start=1):

        print(f"{i}. {paper['title']}")
        print(f"   Year: {paper['year']}")
        print(f"   Citations: {paper['citations']}")
        print(f"   Similarity: {paper['similarity']:.4f}\n")