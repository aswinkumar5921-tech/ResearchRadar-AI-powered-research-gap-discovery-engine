import networkx as nx

G = nx.read_gexf("data/graph/research_graph.gexf")

print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")

degree = nx.degree_centrality(G)

top_nodes = sorted(
    degree.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

print("\nTop 10 Connected Nodes\n")

for node, score in top_nodes:
    print(
        node,
        G.nodes[node],
        score
    )
print("\nCalculating betweenness centrality...")

betweenness = nx.betweenness_centrality(
    G,
    k=500,      # Sample 500 nodes for speed
    seed=42
)

top_bridge_nodes = sorted(
    betweenness.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

print("\nTop Bridge Nodes\n")

for node, score in top_bridge_nodes:
    print(node, G.nodes[node], score)
    
components = list(nx.connected_components(G))

print(f"\nConnected Components: {len(components)}")

largest = max(components, key=len)

print(f"Largest Component Size: {len(largest)}")

import community as community_louvain

partition = community_louvain.best_partition(G)

print(f"\nCommunities Found: {len(set(partition.values()))}")