import pygame
import math
from Graph import Graph

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)

class GraphVisualizer:
    def __init__(self, num_vertices=10, algo='dijkstra', graph_type='dense'):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.algo = algo
        pygame.display.set_caption(f"{self.algo.capitalize()} Algorithm Visualization")
        self.font = pygame.font.SysFont(None, 24)

        # Use the passed graph_type instead of a hardcoded string
        self.graph = Graph(num_vertices, graph_type=graph_type)
        self.positions = self._calculate_positions(num_vertices)
        self.finished = False

        if self.algo == 'dijkstra':
            self.algo_generator = self._dijkstra_step_by_step(0)
            self.current_node = None
            self.visited = set()
            self.distances = [math.inf] * num_vertices
            self.distances[0] = 0
        elif self.algo == 'floyd':
            self.algo_generator = self._floyd_step_by_step()
            self.current_k = None
            self.current_i = None
            self.current_j = None
            self.distances_fw = [[self.graph.matrix[i][j] for j in range(num_vertices)] for i in range(num_vertices)]


    def _calculate_positions(self, num_vertices):
        positions = []
        center_x, center_y = self.width // 2, self.height // 2
        radius = 200
        for i in range(num_vertices):
            angle = 2 * math.pi * i / num_vertices
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions.append((int(x), int(y)))
        return positions

    def _dijkstra_step_by_step(self, source):
        import heapq
        num_vertices = self.graph.num_vertices
        priority_queue = [(0, source)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            self.visited.add(current_vertex)

            yield current_vertex

            if current_distance > self.distances[current_vertex]:
                continue

            for neighbor in range(num_vertices):
                weight = self.graph.matrix[current_vertex][neighbor]
                if weight != math.inf and neighbor != current_vertex:
                    distance = current_distance + weight
                    if distance < self.distances[neighbor]:
                        self.distances[neighbor] = distance
                        heapq.heappush(priority_queue, (distance, neighbor))

    def _floyd_step_by_step(self):
        num_vertices = self.graph.num_vertices
        for k in range(num_vertices):
            for i in range(num_vertices):
                for j in range(num_vertices):
                    yield (k, i, j)
                    if self.distances_fw[i][k] != math.inf and self.distances_fw[k][j] != math.inf:
                        if self.distances_fw[i][k] + self.distances_fw[k][j] < self.distances_fw[i][j]:
                            self.distances_fw[i][j] = self.distances_fw[i][k] + self.distances_fw[k][j]

    def draw_graph(self):
        self.screen.fill(WHITE)
        num_vertices = self.graph.num_vertices

        # Draw edges
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                weight = self.graph.matrix[i][j]
                if weight != math.inf:
                    color = GRAY
                    thickness = 1

                    if self.algo == 'dijkstra' and i in self.visited and j in self.visited:
                        color = BLUE
                        thickness = 2
                    elif self.algo == 'floyd' and self.current_k is not None:
                        # Highlight edges connecting the actively investigated nodes
                        active_nodes = (self.current_k, self.current_i, self.current_j)
                        if i in active_nodes and j in active_nodes:
                            color = BLUE
                            thickness = 2

                    pygame.draw.line(self.screen, color, self.positions[i], self.positions[j], thickness)

                    # Draw weight text
                    mid_x = (self.positions[i][0] + self.positions[j][0]) // 2
                    mid_y = (self.positions[i][1] + self.positions[j][1]) // 2
                    weight_text = self.font.render(str(weight), True, BLACK)
                    self.screen.blit(weight_text, (mid_x, mid_y))

        # Draw vertices
        for i in range(num_vertices):
            if self.algo == 'dijkstra':
                color = RED if i == self.current_node else (GREEN if i in self.visited else GRAY)
                dist_str = str(self.distances[i]) if self.distances[i] != math.inf else "inf"
                text_content = f"{i} ({dist_str})"
            elif self.algo == 'floyd':
                color = GRAY
                if i == self.current_k:
                    color = RED
                elif i == self.current_i:
                    color = BLUE
                elif i == self.current_j:
                    color = GREEN

                # Show distances relative to the current source node `i`
                if self.current_i is not None:
                    dist_str = str(self.distances_fw[self.current_i][i]) if self.distances_fw[self.current_i][i] != math.inf else "inf"
                    text_content = f"{i} ({dist_str})"
                else:
                    text_content = str(i)

            pygame.draw.circle(self.screen, color, self.positions[i], 20)

            # Draw text
            text = self.font.render(text_content, True, BLACK)
            self.screen.blit(text, (self.positions[i][0] - 15, self.positions[i][1] - 35))

        # Floyd info overlay
        if self.algo == 'floyd' and self.current_k is not None:
            info_text = f"k (RED)={self.current_k}, i (BLUE)={self.current_i}, j (GREEN)={self.current_j}"
            info_surf = self.font.render(info_text, True, BLACK)
            self.screen.blit(info_surf, (10, 10))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.finished:
                        try:
                            if self.algo == 'dijkstra':
                                self.current_node = next(self.algo_generator)
                            elif self.algo == 'floyd':
                                self.current_k, self.current_i, self.current_j = next(self.algo_generator)
                        except StopIteration:
                            if self.algo == 'dijkstra':
                                self.current_node = None
                            elif self.algo == 'floyd':
                                self.current_k = self.current_i = self.current_j = None
                            self.finished = True

            self.draw_graph()
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    # Change `algo` to 'dijkstra' or 'floyd'
    # Change `graph_type` to your desired type
    visualizer = GraphVisualizer(num_vertices=6, algo='floyd', graph_type='dense')
    # Press spacebar to step through the algorithm
    visualizer.run()