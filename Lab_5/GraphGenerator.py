from collections import defaultdict

class GraphGenerator:

    def build_adj_list(edges):
        adj = defaultdict(list)

        for u, v, weight in edges:
            adj[u].append((v, weight))
            adj[v].append((u, weight))

        return adj
