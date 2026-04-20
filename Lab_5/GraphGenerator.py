from collections import defaultdict
import random

class GraphGenerator:

    def __init__(self, seed=None, weight_range=(1, 100)):
        self.edges = []
        self.edge_set = set()
        self.weight_range = weight_range
        if seed is not None:
            random.seed(seed)

    def reset(self):
        self.edges.clear()
        self.edge_set.clear()

    def build_adj_list(self):
        adj = defaultdict(list)
        for u, v, weight in self.edges:
            adj[u].append((v, weight))
            adj[v].append((u, weight))
        return adj

    def _add_edge(self, u, v, weight):
        u, v = sorted((u, v))
        if (u, v) in self.edge_set:
            return False
        self.edges.append((u, v, weight))
        self.edge_set.add((u, v))
        return True

    def add_edges(self, n, target_e, seed=None, weight_range=None):
        if seed is not None:
            random.seed(seed)
        wr = weight_range if weight_range is not None else self.weight_range
        while len(self.edges) < target_e:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u == v:
                continue
            weight = random.randint(wr[0], wr[1])
            self._add_edge(u, v, weight)

    def generate_connected(self, n, target_e, seed=None, weight_range=None):
        if target_e < n - 1:
            raise ValueError("target_e must be at least n - 1 to be connected")
        max_edges = n * (n - 1) // 2
        if target_e > max_edges:
            raise ValueError(f"target_e cannot exceed {max_edges} for n={n}")

        if seed is not None:
            random.seed(seed)
        wr = weight_range if weight_range is not None else self.weight_range

        self.reset()

        # create a random spanning tree (chain after shuffle)
        nodes = list(range(n))
        random.shuffle(nodes)
        for i in range(1, n):
            u = nodes[i - 1]
            v = nodes[i]
            weight = random.randint(wr[0], wr[1])
            self._add_edge(u, v, weight)

        # add remaining random edges
        self.add_edges(n, target_e, seed=None, weight_range=wr)
