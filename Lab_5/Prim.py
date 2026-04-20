from typing import List, Tuple
import heapq

def prim(n: int, edges: List[Tuple[int, int, int]]) -> Tuple[List[Tuple[int, int, int]], int]:
    """
    Compute MST using Prim's algorithm.
    Args:
        n: number of nodes (0..n-1)
        edges: list of (u, v, weight)
    Returns:
        (mst_edges, total_weight)
    Raises:
        ValueError if graph is disconnected
    """
    if n == 0:
        return [], 0

    # build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    visited = [False] * n
    mst_edges: List[Tuple[int, int, int]] = []
    total_weight = 0
    heap: List[Tuple[int, int, int]] = []

    # start from node 0
    visited[0] = True
    for to, wt in adj[0]:
        heapq.heappush(heap, (wt, 0, to))

    while heap and len(mst_edges) < n - 1:
        w, u, v = heapq.heappop(heap)
        if visited[v]:
            continue
        visited[v] = True
        mst_edges.append((u, v, w))
        total_weight += w
        for to, wt in adj[v]:
            if not visited[to]:
                heapq.heappush(heap, (wt, v, to))

    if len(mst_edges) != n - 1:
        raise ValueError("Graph is not connected; MST not found")

    return mst_edges, total_weight

if __name__ == "__main__":
    sample_edges = [(0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4)]
    mst, w = prim(4, sample_edges)
    print("MST edges:", mst)
    print("Total weight:", w)