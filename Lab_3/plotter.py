import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, results):
        self.results = results  # dictionary {label: [(n, avg_time), ...]}

    def plot(self, title="Algorithm Comparison"):
        plt.figure(figsize=(8, 6))
        for label, data in self.results.items():
            sizes = [n for n, t in data]
            times = [t for n, t in data]
            plt.plot(sizes, times, marker="o", label=label)
        plt.xlabel("Number of nodes")
        plt.ylabel("Execution time (s)")
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_by_graph_type(self, results_by_type, algorithm_label):
        plt.figure(figsize=(8, 6))
        for graph_type, algo_results in results_by_type.items():
            if algorithm_label not in algo_results:
                continue
            data = algo_results[algorithm_label]
            sizes = [n for n, t in data]
            times = [t for n, t in data]
            plt.plot(sizes, times, marker="o", label=graph_type)
        plt.xlabel("Number of nodes")
        plt.ylabel("Execution time (s)")
        plt.title(f"{algorithm_label} by Graph Type")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_heatmap(self, results_by_type, algorithm_label, sizes):
        graph_types = list(results_by_type.keys())
        heatmap = []
        for graph_type in graph_types:
            data = results_by_type[graph_type].get(algorithm_label, [])
            time_map = {n: t for n, t in data}
            heatmap.append([time_map.get(n, 0.0) for n in sizes])

        fig, ax = plt.subplots(figsize=(9, 4))
        cax = ax.imshow(heatmap, aspect="auto", cmap="viridis")
        ax.set_xticks(range(len(sizes)))
        ax.set_xticklabels(sizes)
        ax.set_yticks(range(len(graph_types)))
        ax.set_yticklabels(graph_types)
        ax.set_xlabel("Number of nodes")
        ax.set_ylabel("Graph type")
        ax.set_title(f"{algorithm_label} Heatmap")
        fig.colorbar(cax, ax=ax, label="Execution time (s)")
        plt.tight_layout()
        plt.show()