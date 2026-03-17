import pygame
import math
import time
from graph_generator import generate_graph


# Custom exceptions to control flow from inside the algorithms
class ResetSignal(Exception): pass


class NewGraphSignal(Exception): pass


class GraphVisualizer:
    def __init__(self, start_graph=None):
        pygame.init()
        self.width, self.height = 1024, 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Graph Traversal Visualizer")

        self.font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)

        # State
        self.n = 20  # default size
        self.delay = 0.2
        self.paused = False
        self.visited_sequence = []
        self.current_node = None

        # Load initial graph
        if start_graph:
            self.set_graph(start_graph)
            self.n = len(start_graph)
        else:
            self.regenerate_graph()

    def regenerate_graph(self):
        """Generates a new graph based on current N."""
        # Using 3 edges per node as a default for visualization
        self.set_graph(generate_graph(self.n, edges_per_node=3))

    def set_graph(self, graph):
        self.graph = graph
        self.n = len(graph)
        self.positions = self._generate_positions()
        self.visited_sequence = []
        self.current_node = None

    def _generate_positions(self):
        """Arranges nodes in a circle."""
        positions = {}
        center_x, center_y = self.width // 2, self.height // 2
        # Radius adjusts based on window size
        radius = min(self.width, self.height) // 2 - 100

        for i in range(self.n):
            angle = 2 * math.pi * i / self.n
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            positions[i] = (x, y)
        return positions

    def draw(self):
        self.screen.fill((255, 255, 255))

        # 1. Draw UI / Instructions
        instructions = [
            f"Nodes: {self.n} (+/- to resize, 'G' to regenerate)",
            f"Speed Delay: {self.delay:.2f}s (UP/DOWN)",
            "SPACE: Pause/Resume | RIGHT: Step",
            "R: Restart Traversal"
        ]
        for i, text in enumerate(instructions):
            surf = self.font.render(text, True, (50, 50, 50))
            self.screen.blit(surf, (10, 10 + i * 25))

        if self.paused:
            status = self.title_font.render("PAUSED", True, (200, 0, 0))
            self.screen.blit(status, (self.width - 120, 10))

        # 2. Draw Edges
        for u, neighbors in self.graph.items():
            for v in neighbors:
                if u in self.positions and v in self.positions:
                    start = self.positions[u]
                    end = self.positions[v]
                    pygame.draw.line(self.screen, (200, 200, 200), start, end, 1)

        # 3. Draw Nodes
        for node, pos in self.positions.items():
            color = (100, 100, 255)  # Default Blue

            if node in self.visited_sequence:
                color = (100, 200, 100)  # Visited Green

            if node == self.current_node:
                color = (255, 100, 100)  # Current Red

            pygame.draw.circle(self.screen, color, pos, 15)

            # Numeric label
            label = self.font.render(str(node), True, (0, 0, 0))
            self.screen.blit(label, (pos[0] - 5, pos[1] - 10))

        pygame.display.flip()

    def process_inputs(self):
        """Handles key presses."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_UP:
                    self.delay = max(0.01, self.delay - 0.05)
                elif event.key == pygame.K_DOWN:
                    self.delay += 0.05
                elif event.key == pygame.K_RIGHT:
                    return "step"
                elif event.key == pygame.K_r:
                    raise ResetSignal()
                elif event.key == pygame.K_g:
                    raise NewGraphSignal()
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    self.n += 5
                    raise NewGraphSignal()
                elif event.key == pygame.K_MINUS:
                    self.n = max(5, self.n - 5)
                    raise NewGraphSignal()
        return None

    def visit_callback(self, node):
        """Passed to BFS/DFS. Handles drawing and waiting."""
        self.visited_sequence.append(node)
        self.current_node = node
        self.draw()

        start_time = time.time()

        # Wait Loop (replaces simple sleep)
        while True:
            action = self.process_inputs()

            if self.paused:
                # If paused, wait indefinitely until 'step' is pressed or unpaused
                if action == "step":
                    break
            else:
                # If running, break after delay
                if time.time() - start_time > self.delay:
                    break

            # Redraw to update UI (like speed text) while waiting
            self.draw()
            time.sleep(0.01)  # constant small sleep to save CPU

    def animate_traversal(self, algorithm_func, start_node=0):
        running = True
        while running:
            # Reset visual state
            self.visited_sequence = []
            self.current_node = None

            try:
                # Run the blocking algorithm
                # Ensure start_node is valid for current graph size
                valid_start = start_node if start_node < self.n else 0
                algorithm_func(self.graph, valid_start, visit_callback=self.visit_callback)

                # Algorithm Finished - Wait for user
                self.current_node = None
                self.draw()
                while True:
                    self.process_inputs()
                    time.sleep(0.05)

            except ResetSignal:
                # User pressed 'R', loop restarts with same graph
                continue
            except NewGraphSignal:
                # User pressed 'G' or '+/-', regenerate and restart
                self.regenerate_graph()
                continue
