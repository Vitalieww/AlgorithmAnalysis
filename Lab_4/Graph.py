import random
import math

class Graph:
    def __init__(self, num_vertices, graph_type='sparse'):
        self.num_vertices = num_vertices
        self.graph_type = graph_type
        self.matrix = self._generate_graph()

    def _generate_graph(self):
        matrix = [[math.inf] * self.num_vertices for _ in range(self.num_vertices)]
        for i in range(self.num_vertices):
            matrix[i][i] = 0

        if self.graph_type in ['sparse', 'dense']:
            probability = 0.9 if self.graph_type == 'dense' else 0.2
            for i in range(self.num_vertices):
                for j in range(i + 1, self.num_vertices):
                    if random.random() < probability:
                        weight = random.randint(1, 20)
                        matrix[i][j] = weight
                        matrix[j][i] = weight

        elif self.graph_type == 'tree':
            for i in range(1, self.num_vertices):
                j = random.randint(0, i - 1)  # Connect to a previously added node
                weight = random.randint(1, 20)
                matrix[i][j] = weight
                matrix[j][i] = weight

        elif self.graph_type == 'path':
            for i in range(self.num_vertices - 1):
                weight = random.randint(1, 20)
                matrix[i][i + 1] = weight
                matrix[i + 1][i] = weight

        elif self.graph_type == 'disconnected':
            num_components = 3
            probability = 0.4
            for i in range(self.num_vertices):
                for j in range(i + 1, self.num_vertices):
                    # Only connect nodes strictly within the same mathematical component bucket
                    if i % num_components == j % num_components and random.random() < probability:
                        weight = random.randint(1, 20)
                        matrix[i][j] = weight
                        matrix[j][i] = weight

        return matrix