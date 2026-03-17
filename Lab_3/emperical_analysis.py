import time
from graph_generator import generate_graph


class EmpiricalAnalysis:
    def __init__(self, sizes, edges_per_node=10, repeats=3):
        self.sizes = sizes
        self.edges_per_node = edges_per_node
        self.repeats = repeats
        self.results = {}  # flat results: {label: [(n, avg_time), ...]}
        self.results_by_type = {}  # nested results: {graph_type: {label: [(n, avg_time)]}}

    def run_algorithm(self, algorithm, label):
        return self.run_algorithm_with_builder(algorithm, label, self._default_graph_builder)

    def run_algorithm_with_builder(self, algorithm, label, graph_builder):
        results = []
        for n in self.sizes:
            graph = graph_builder(n)
            avg_time = self._time_algorithm(algorithm, graph)
            results.append((n, avg_time))
            print(f"{label}: n={n}, avg_time={avg_time:.6f}s")
        self.results[label] = results
        return results

    def run_algorithm_by_graph_types(self, algorithm, label, graph_builders):
        for graph_type, builder in graph_builders.items():
            results = []
            for n in self.sizes:
                graph = builder(n)
                avg_time = self._time_algorithm(algorithm, graph)
                results.append((n, avg_time))
                print(f"{label} ({graph_type}): n={n}, avg_time={avg_time:.6f}s")

            self.results.setdefault(f"{label} ({graph_type})", results)
            self.results_by_type.setdefault(graph_type, {})[label] = results

    def _time_algorithm(self, algorithm, graph):
        total_time = 0.0
        for _ in range(self.repeats):
            start_time = time.perf_counter()
            algorithm(graph, 0)
            end_time = time.perf_counter()
            total_time += end_time - start_time
        return total_time / self.repeats

    def _default_graph_builder(self, n):
        return generate_graph(n, self.edges_per_node)