from algorithm_analysis import AlgorithmAnalyzer
from algorithms import quicksort, mergesort, heapsort, introsort

def main():
    analyzer = AlgorithmAnalyzer()

    algorithms = [quicksort, mergesort, heapsort, introsort]
    sizes = [100, 500, 1000, 2000]
    input_types = ["random", "sorted","almost_sorted", "reverse","duplicates"]
    repeat = 3  # average over 3 runs to reduce noise

    # Run experiments, print results to terminal and show matplotlib plots
    analyzer.run_multiple(algorithms, sizes, input_types=input_types, repeat=repeat, show_plot=True)

if __name__ == "__main__":
    main()