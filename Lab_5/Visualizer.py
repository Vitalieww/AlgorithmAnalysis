import sys
import math
import random
import heapq
import pygame

from GraphGenerator import GraphGenerator
from Kruskal import UnionFind

# --- Config ---
WIDTH, HEIGHT = 800, 600
FPS = 30  # Increased FPS for input responsiveness, animation is now manual step
NODE_RADIUS = 12

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)


class Visualizer:
    def __init__(self, num_nodes=15, density=0.3):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MST Visualizer: Kruskal & Prim")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.weight_font = pygame.font.SysFont(None, 18)

        self.num_nodes = num_nodes
        self.density = density
        self.nodes = []
        self.edges = []

        self.algorithm_generator = None
        self.current_edge = None
        self.mst_edges = []
        self.state_message = "Press [K] Kruskal, [P] Prim, [R] Reset"

        self.generate_graph()

    def generate_graph(self):
        max_edges = self.num_nodes * (self.num_nodes - 1) // 2
        target_e = max(self.num_nodes - 1, int(self.density * max_edges))

        gg = GraphGenerator()
        gg.generate_connected(self.num_nodes, target_e)
        self.edges = list(gg.edges)

        self.nodes = []
        pad = 50
        for _ in range(self.num_nodes):
            x = random.randint(pad, WIDTH - pad)
            y = random.randint(pad, HEIGHT - pad)
            self.nodes.append((x, y))

        self.reset_state()

    def reset_state(self):
        self.algorithm_generator = None
        self.current_edge = None
        self.mst_edges = []
        self.state_message = "Press [K] Kruskal, [P] Prim, [R] Reset"

    def kruskal_generator(self):
        self.state_message = "Kruskal's: Press [SPACE] to step"
        uf = UnionFind(self.num_nodes)
        sorted_edges = sorted(self.edges, key=lambda e: e[2])

        for u, v, w in sorted_edges:
            self.current_edge = (u, v)

            if uf.union(u, v):
                self.mst_edges.append((u, v, w))

            yield  # Single yield per edge evaluation

            if len(self.mst_edges) == self.num_nodes - 1:
                break

        self.current_edge = None
        self.state_message = "Kruskal's Algorithm Finished"
        yield

    def prim_generator(self):
        self.state_message = "Prim's: Press [SPACE] to step"
        adj = [[] for _ in range(self.num_nodes)]
        for u, v, w in self.edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        visited = [False] * self.num_nodes
        heap = []

        visited[0] = True
        for to, wt in adj[0]:
            heapq.heappush(heap, (wt, 0, to))

        while heap and len(self.mst_edges) < self.num_nodes - 1:
            w, u, v = heapq.heappop(heap)
            self.current_edge = (u, v)

            if not visited[v]:
                visited[v] = True
                self.mst_edges.append((u, v, w))
                for to, wt in adj[v]:
                    if not visited[to]:
                        heapq.heappush(heap, (wt, v, to))

            yield  # Single yield per edge evaluation

        self.current_edge = None
        self.state_message = "Prim's Algorithm Finished"
        yield

    def draw(self):
        self.screen.fill(WHITE)

        for u, v, w in self.edges:
            pygame.draw.line(self.screen, GRAY, self.nodes[u], self.nodes[v], 1)

        for u, v, w in self.mst_edges:
            pygame.draw.line(self.screen, GREEN, self.nodes[u], self.nodes[v], 4)

        if self.current_edge:
            u, v = self.current_edge
            pygame.draw.line(self.screen, RED, self.nodes[u], self.nodes[v], 4)

        for u, v, w in self.edges:
            mid_x = (self.nodes[u][0] + self.nodes[v][0]) // 2
            mid_y = (self.nodes[u][1] + self.nodes[v][1]) // 2
            text_surf = self.weight_font.render(str(w), True, DARK_GRAY)
            text_rect = text_surf.get_rect(center=(mid_x, mid_y))
            bg_rect = text_rect.inflate(4, 4)
            pygame.draw.rect(self.screen, WHITE, bg_rect)
            self.screen.blit(text_surf, text_rect)

        for i, pos in enumerate(self.nodes):
            pygame.draw.circle(self.screen, BLUE, pos, NODE_RADIUS)
            text = self.font.render(str(i), True, WHITE)
            text_rect = text.get_rect(center=pos)
            self.screen.blit(text, text_rect)

        text_surface = self.font.render(self.state_message, True, BLACK)
        self.screen.blit(text_surface, (10, 10))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.generate_graph()
                    elif event.key == pygame.K_k:
                        self.reset_state()
                        self.algorithm_generator = self.kruskal_generator()
                    elif event.key == pygame.K_p:
                        self.reset_state()
                        self.algorithm_generator = self.prim_generator()
                    elif event.key == pygame.K_SPACE:
                        if self.algorithm_generator:
                            try:
                                next(self.algorithm_generator)
                            except StopIteration:
                                self.algorithm_generator = None

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    visualizer = Visualizer(num_nodes=15, density=0.2)
    visualizer.run()