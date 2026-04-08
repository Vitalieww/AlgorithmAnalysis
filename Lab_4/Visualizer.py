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
    def __init__(self, num_vertices=10):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dijkstra Algorithm Visualization")
        self.font = pygame.font.SysFont(None, 24)

        self.graph = Graph(num_vertices, is_dense=False)
        self.positions = self._calculate_positions(num_vertices)

        # Generator for step-by-step execution
        self.algo_generator = self._dijkstra_step_by_step(0)
        self.current_node = None
        self.visited = set()
        self.distances = [math.inf] * num_vertices
        self.distances[0] = 0
        self.finished = False

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

            # Yield current state for visualization
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
                    if i in self.visited and j in self.visited:
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
            color = RED if i == self.current_node else (GREEN if i in self.visited else GRAY)
            pygame.draw.circle(self.screen, color, self.positions[i], 20)

            # Draw distance and node id
            dist_str = str(self.distances[i]) if self.distances[i] != math.inf else "inf"
            text = self.font.render(f"{i} ({dist_str})", True, BLACK)
            self.screen.blit(text, (self.positions[i][0] - 15, self.positions[i][1] - 35))

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
                            self.current_node = next(self.algo_generator)
                        except StopIteration:
                            self.current_node = None
                            self.finished = True

            self.draw_graph()
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    visualizer = GraphVisualizer(num_vertices=8)
    # Press spacebar to step through the algorithm
    visualizer.run()