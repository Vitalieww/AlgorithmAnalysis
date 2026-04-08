import time
import matplotlib.pyplot as plt
from Graph import Graph
from PathFinder import PathFinder

class Analyzer:
    def __init__(self, vertex_counts):
        self.vertex_counts = vertex_counts
        self.graph_types = ['sparse', 'dense', 'tree', 'path', 'disconnected']
        self.dijkstra_results = {g_type: [] for g_type in self.graph_types}
        self.floyd_results = {g_type: [] for g_type in self.graph_types}

    def run_analysis(self):
        for v in self.vertex_counts:
            for g_type in self.graph_types:
                graph = Graph(v, graph_type=g_type)

                # Measure Dijkstra
                start = time.perf_counter()
                PathFinder.dijkstra_all_pairs(graph)
                self.dijkstra_results[g_type].append(time.perf_counter() - start)

                # Measure Floyd-Warshall
                start = time.perf_counter()
                PathFinder.floyd_warshall(graph)
                self.floyd_results[g_type].append(time.perf_counter() - start)

        self._print_results()
        self._plot_results()

    def _print_results(self):
        print("+--------------------------+------+-----------+")
        print("| Algorithm & Type         | Size | Time (s)  |")
        print("+--------------------------+------+-----------+")
        for i, v in enumerate(self.vertex_counts):
            for g_type in self.graph_types:
                d_time = self.dijkstra_results[g_type][i]
                f_time = self.floyd_results[g_type][i]
                print(f"| Dijkstra ({g_type[:5]:>5})    | {v:<4} | {d_time:<9.6f} |")
                print(f"| Floyd-W. ({g_type[:5]:>5})    | {v:<4} | {f_time:<9.6f} |")
        print("+--------------------------+------+-----------+")

    def _plot_results(self):
        plt.figure(figsize=(14, 6))

        # Dijkstra Plot
        plt.subplot(1, 2, 1)
        for g_type in self.graph_types:
            plt.plot(self.vertex_counts, self.dijkstra_results[g_type], label=g_type, marker='o')
        plt.title('Dijkstra (All-Pairs) Performance')
        plt.xlabel('Number of Vertices')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)

        # Floyd-Warshall Plot
        plt.subplot(1, 2, 2)
        for g_type in self.graph_types:
            plt.plot(self.vertex_counts, self.floyd_results[g_type], label=g_type, marker='s')
        plt.title('Floyd-Warshall Performance')
        plt.xlabel('Number of Vertices')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    node_sizes = [10, 25, 50, 75, 100]
    analyzer = Analyzer(node_sizes)
    analyzer.run_analysis()