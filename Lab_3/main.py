from emperical_analysis import EmpiricalAnalysis
from dfs import dfs
from bfs import bfs
from plotter import Plotter
from graph_generator import (
	generate_dense_graph,
	generate_disconnected_graph,
	generate_path_graph,
	generate_sparse_graph,
	generate_tree_graph,
)

# Experiment setup
sizes = [100, 500, 1000, 2000]
analysis = EmpiricalAnalysis(sizes, edges_per_node=10, repeats=5)

graph_builders = {
	"Sparse": lambda n: generate_sparse_graph(n, edges_per_node=10),
	"Dense": lambda n: generate_dense_graph(n, density=0.3),
	"Tree": generate_tree_graph,
	"Path": generate_path_graph,
	"Disconnected": lambda n: generate_disconnected_graph(n, components=3, edges_per_node=3),
}

# Run experiments for all graph types
analysis.run_algorithm_by_graph_types(dfs, "DFS", graph_builders)
analysis.run_algorithm_by_graph_types(bfs, "BFS", graph_builders)

# Plot results
plotter = Plotter(analysis.results)
plotter.plot(title="DFS vs BFS Execution Time (All Graph Types)")
plotter.plot_by_graph_type(analysis.results_by_type, "DFS")
plotter.plot_by_graph_type(analysis.results_by_type, "BFS")
plotter.plot_heatmap(analysis.results_by_type, "DFS", sizes)
plotter.plot_heatmap(analysis.results_by_type, "BFS", sizes)