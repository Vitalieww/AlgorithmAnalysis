import heapq
import math

class PathFinder:
    @staticmethod
    def dijkstra_all_pairs(graph):
        num_vertices = graph.num_vertices
        all_shortest_paths = []

        for source in range(num_vertices):
            distances = [math.inf] * num_vertices
            distances[source] = 0
            priority_queue = [(0, source)]

            while priority_queue:
                current_distance, current_vertex = heapq.heappop(priority_queue)

                if current_distance > distances[current_vertex]:
                    continue

                for neighbor in range(num_vertices):
                    weight = graph.matrix[current_vertex][neighbor]
                    if weight != math.inf and neighbor != current_vertex:
                        distance = current_distance + weight
                        if distance < distances[neighbor]:
                            distances[neighbor] = distance
                            heapq.heappush(priority_queue, (distance, neighbor))

            all_shortest_paths.append(distances)
        return all_shortest_paths

    @staticmethod
    def floyd_warshall(graph):
        num_vertices = graph.num_vertices
        distances = [[graph.matrix[i][j] for j in range(num_vertices)] for i in range(num_vertices)]

        for k in range(num_vertices):
            for i in range(num_vertices):
                for j in range(num_vertices):
                    if distances[i][k] != math.inf and distances[k][j] != math.inf:
                        distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

        return distances