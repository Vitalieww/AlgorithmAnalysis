
def dfs(graph, start, visit_callback=lambda x: None):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            visit_callback(node)  # callback for optional recording/visualization
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
    return visited
