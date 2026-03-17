import random


def generate_sparse_graph(n, edges_per_node):
    """Generates a sparse undirected graph as an adjacency list."""
    graph = {i: set() for i in range(n)}
    for node in range(n):
        while len(graph[node]) < edges_per_node:
            neighbor = random.randint(0, n - 1)
            if neighbor != node:
                graph[node].add(neighbor)
                graph[neighbor].add(node)  # undirected
    return {node: list(neighbors) for node, neighbors in graph.items()}


def generate_dense_graph(n, density=0.3):
    """Generates a dense undirected graph using edge probability density."""
    density = max(0.0, min(1.0, density))
    graph = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < density:
                graph[i].add(j)
                graph[j].add(i)
    return {node: list(neighbors) for node, neighbors in graph.items()}


def generate_tree_graph(n):
    """Generates a random tree with n nodes (connected, acyclic)."""
    graph = {i: set() for i in range(n)}
    for node in range(1, n):
        parent = random.randint(0, node - 1)
        graph[node].add(parent)
        graph[parent].add(node)
    return {node: list(neighbors) for node, neighbors in graph.items()}


def generate_path_graph(n):
    """Generates a simple path graph: 0-1-2-...-(n-1)."""
    graph = {i: set() for i in range(n)}
    for node in range(n - 1):
        graph[node].add(node + 1)
        graph[node + 1].add(node)
    return {node: list(neighbors) for node, neighbors in graph.items()}


def generate_disconnected_graph(n, components=3, edges_per_node=3):
    """Generates a disconnected graph by creating isolated sparse components."""
    components = max(2, min(components, n))
    sizes = _split_sizes(n, components)

    graph = {i: set() for i in range(n)}
    start = 0
    for size in sizes:
        nodes = list(range(start, start + size))
        subgraph = generate_sparse_graph(size, edges_per_node)
        for local_node, neighbors in subgraph.items():
            global_node = nodes[local_node]
            for neighbor in neighbors:
                graph[global_node].add(nodes[neighbor])
        start += size
    return {node: list(neighbors) for node, neighbors in graph.items()}


def _split_sizes(n, components):
    """Splits n into component sizes as evenly as possible."""
    base = n // components
    remainder = n % components
    sizes = [base + (1 if i < remainder else 0) for i in range(components)]
    return [size for size in sizes if size > 0]


def generate_graph(n, edges_per_node):
    """Backward-compatible alias for sparse graphs."""
    return generate_sparse_graph(n, edges_per_node)