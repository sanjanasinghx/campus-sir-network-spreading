"""
Campus contact network: node populations, edges, row-normalised weight matrix.

Node order (index 0-8): H1, H2, H3, D, L, A, Lab, S, G
"""
import numpy as np
import networkx as nx

# Node definitions
NODES = ["H1", "H2", "H3", "D", "L", "A", "Lab", "S", "G"]
IDX   = {n: i for i, n in enumerate(NODES)}

POPULATIONS = np.array([320, 280, 260, 450, 180, 520, 240, 160, 120], dtype=float)
N_TOTAL = POPULATIONS.sum()   # 2530

# Edges (undirected, weighted)
EDGES = [
    ("H1", "D",   0.8),
    ("H2", "D",   0.9),
    ("H3", "D",   0.7),
    ("H1", "A",   0.4),
    ("H2", "A",   0.5),
    ("H3", "A",   0.3),
    ("D",  "A",   1.0),
    ("D",  "L",   0.5),
    ("D",  "S",   0.4),
    ("A",  "L",   0.7),
    ("A",  "Lab", 0.8),
    ("A",  "G",   0.4),
    ("Lab","G",   0.3),
    ("L",  "G",   0.2),
]

def build_graph() -> nx.Graph:
    G = nx.Graph()
    for node, pop in zip(NODES, POPULATIONS):
        G.add_node(node, population=pop)
    for u, v, w in EDGES:
        G.add_edge(u, v, weight=w)
    return G

# Row-normalised weight matrix W_hat (9x9)
def build_W_hat() -> np.ndarray:
    n = len(NODES)
    W = np.zeros((n, n))
    for u, v, w in EDGES:
        i, j = IDX[u], IDX[v]
        W[i, j] = w
        W[j, i] = w

    row_sums = W.sum(axis=1, keepdims=True)
    # guard against isolated nodes
    row_sums = np.where(row_sums == 0, 1.0, row_sums)
    W_hat = W / row_sums
    return W_hat

# Structural measures (part b)
def compute_measures(G: nx.Graph) -> dict:
    deg   = dict(G.degree(weight="weight"))
    bc    = nx.betweenness_centrality(G, weight="weight", normalized=True)
    cc    = nx.closeness_centrality(G, distance="weight")
    return {"weighted_degree": deg, "betweenness": bc, "closeness": cc}


G_CAMPUS = build_graph()
W_HAT    = build_W_hat()

assert np.allclose(W_HAT.sum(axis=1), 1.0), "Row sums of W_hat are not all 1!"

if __name__ == "__main__":
    print("Nodes:", NODES)
    print("Populations:", POPULATIONS)
    print("N_total:", N_TOTAL)
    print("\nW_hat (row sums):", W_HAT.sum(axis=1))
    m = compute_measures(G_CAMPUS)
    print("\nWeighted degree:", {k: round(v,3) for k,v in m["weighted_degree"].items()})
    print("Betweenness:    ", {k: round(v,3) for k,v in m["betweenness"].items()})
