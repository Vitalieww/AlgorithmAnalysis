from typing import List, Tuple

class UnionFind:
    """Disjoint set with path compression and union by rank."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        else:
            self.parent[ry] = rx
            if self.rank[rx] == self.rank[ry]:
                self.rank[rx] += 1
        return True

def kruskal(n: int, edges: List[Tuple[int, int, int]]) -> Tuple[List[Tuple[int, int, int]], int]:
    """
    Compute MST using Kruskal's algorithm.
    Args:
        n: number of nodes (nodes assumed 0..n-1)
        edges: list of (u, v, weight)
    Returns:
        (mst_edges, total_weight)
    """
    uf = UnionFind(n)
    mst_edges: List[Tuple[int, int, int]] = []
    total_weight = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            if len(mst_edges) == n - 1:
                break
    return mst_edges, total_weight

if __name__ == "__main__":
    # tiny sanity check
    sample_edges = [(0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4)]
    mst, w = kruskal(4, sample_edges)
    print("MST edges:", mst)
    print("Total weight:", w)