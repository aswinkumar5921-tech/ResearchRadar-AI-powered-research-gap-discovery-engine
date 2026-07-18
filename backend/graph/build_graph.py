import sqlite3
import networkx as nx

DB_PATH = "data/sqlite/research.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

G = nx.Graph()

# -------------------------
# Add Paper Nodes
# -------------------------
cursor.execute("SELECT id, title FROM papers")

for paper_id, title in cursor.fetchall():
    G.add_node(
        f"P{paper_id}",
        type="paper",
        title=title
    )

# -------------------------
# Add Author Nodes + Edges
# -------------------------
cursor.execute("""
SELECT a.id, a.name, pa.paper_id
FROM authors a
JOIN paper_authors pa
ON a.id = pa.author_id
""")

for author_id, name, paper_id in cursor.fetchall():

    G.add_node(
        f"A{author_id}",
        type="author",
        name=name
    )

    G.add_edge(
        f"A{author_id}",
        f"P{paper_id}",
        relation="WROTE"
    )

# -------------------------
# Add Concept Nodes + Edges
# -------------------------
cursor.execute("""
SELECT c.id, c.name, pc.paper_id
FROM concepts c
JOIN paper_concepts pc
ON c.id = pc.concept_id
""")

for concept_id, name, paper_id in cursor.fetchall():

    G.add_node(
        f"C{concept_id}",
        type="concept",
        name=name
    )

    G.add_edge(
        f"P{paper_id}",
        f"C{concept_id}",
        relation="HAS_CONCEPT"
    )

print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")

conn.close()

import os

os.makedirs("data/graph", exist_ok=True)

nx.write_gexf(G, "data/graph/research_graph.gexf")

print("Graph saved successfully.")