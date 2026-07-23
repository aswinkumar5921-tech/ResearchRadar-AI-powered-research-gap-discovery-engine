import networkx as nx

GRAPH_PATH = "data/graph/research_graph.gexf"

G = nx.read_gexf(GRAPH_PATH)

print(f"Loaded graph with {G.number_of_nodes()} nodes")


betweenness = nx.betweenness_centrality(
    G,
    k=500,
    normalized=True,
    seed=42
)

top_nodes = sorted(
    betweenness.items(),
    key=lambda x: x[1],
    reverse=True
)[:20]

import sqlite3

conn = sqlite3.connect("data/sqlite/research.db")
cursor = conn.cursor()

print("\nTop Bridge Nodes\n")

for node, score in top_nodes:

    if node.startswith("P"):

        paper_id = int(node[1:])

        cursor.execute(
            "SELECT title FROM papers WHERE id=?",
            (paper_id,)
        )

        result = cursor.fetchone()

        name = result[0] if result else node

    elif node.startswith("C"):

        concept_id = int(node[1:])

        cursor.execute(
            "SELECT name FROM concepts WHERE id=?",
            (concept_id,)
        )

        result = cursor.fetchone()

        name = result[0] if result else node

    else:
        name = node

    print(f"{name[:70]:70} {score:.6f}")

conn.close()