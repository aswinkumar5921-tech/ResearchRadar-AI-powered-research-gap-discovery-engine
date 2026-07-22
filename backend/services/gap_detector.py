import sqlite3
import numpy as np
import networkx as nx
from fastembed import TextEmbedding
from sklearn.metrics.pairwise import cosine_similarity

print("Loading resources...")

# Load graph
G = nx.read_gexf("data/graph/research_graph.gexf")

# Load vectors
paper_ids = np.load("data/embeddings/paper_ids.npy")
paper_vectors = np.load("data/embeddings/paper_vectors.npy")

# Load embedding model
model = TextEmbedding()

query = input("Enter research topic: ")

query_vector = np.array(
    list(model.embed([query]))[0]
).reshape(1, -1)

similarities = cosine_similarity(
    query_vector,
    paper_vectors
)[0]

top_indices = np.argsort(similarities)[::-1][:20]

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

results = []

for idx in top_indices:

    paper_id = int(paper_ids[idx])

    cursor.execute("""
        SELECT title,
               publication_year,
               cited_by_count
        FROM papers
        WHERE id=?
    """, (paper_id,))

    paper = cursor.fetchone()

    if not paper:
        continue

    title, year, citations = paper

    graph_node = f"P{paper_id}"

    degree = G.degree(graph_node) if G.has_node(graph_node) else 0

    results.append({
        "title": title,
        "year": year,
        "citations": citations,
        "similarity": similarities[idx],
        "degree": degree
    })


print("\nTop Research Opportunities\n")

for i, paper in enumerate(results, start=1):

    print("=" * 70)

    print(f"{i}. {paper['title']}")

    print(f"Year: {paper['year']}")

    print(f"Citations: {paper['citations']}")

    print(f"Semantic Similarity: {paper['similarity']:.3f}")

    print(f"Graph Degree: {paper['degree']}")
    
conn.close()