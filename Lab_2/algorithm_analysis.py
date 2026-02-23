import random
import time
import matplotlib.pyplot as plt

class Comparable:
    def __init__(self, value, counter):
        self.value = value
        self.counter = counter  # shared Counter object

    def __lt__(self, other):
        self.counter.count += 1
        return self.value < other.value

    def __le__(self, other):
        self.counter.count += 1
        return self.value <= other.value

    def __gt__(self, other):
        self.counter.count += 1
        return self.value > other.value

    def __ge__(self, other):
        self.counter.count += 1
        return self.value >= other.value

class Counter:
    def __init__(self):
        self.count = 0

    def reset(self):
        self.count = 0



class AlgorithmAnalyzer:
    def __init__(self):
        self.results = []

    def run_experiment(self, algorithm, input_data, input_type, size):
        counter = Counter()
        arr = [Comparable(v, counter) for v in input_data]

        start_time = time.perf_counter()
        algorithm(arr)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        comparisons = counter.count

        result = {
            "algorithm": algorithm.__name__,
            "input_type": input_type,
            "size": size,
            "time": elapsed_time,
            "comparisons": comparisons
        }
        self.results.append(result)
        return result

    def run_multiple(self, algorithms, sizes, input_types="random", repeat=1, show_plot=True):
        """
        Run multiple algorithms across given sizes and input types.
        - algorithms: list of callables (in-place sorting functions)
        - sizes: list of integer sizes
        - input_types: str or list of input_type strings accepted by generate_input
        - repeat: number of times to run each configuration (results are averaged)
        - show_plot: whether to display matplotlib plots
        """
        if isinstance(input_types, str):
            input_types = [input_types]

        for input_type in input_types:
            # collect per-algorithm series
            series = {alg.__name__: {"sizes": [], "time": [], "comparisons": []} for alg in algorithms}

            for size in sizes:
                for alg in algorithms:
                    total_time = 0.0
                    total_comps = 0
                    for _ in range(repeat):
                        input_data = generate_input(size, input_type)
                        res = self.run_experiment(alg, input_data, input_type, size)
                        total_time += res["time"]
                        total_comps += res["comparisons"]
                    avg_time = total_time / repeat
                    avg_comps = total_comps / repeat

                    name = alg.__name__
                    series[name]["sizes"].append(size)
                    series[name]["time"].append(avg_time)
                    series[name]["comparisons"].append(avg_comps)

            # Print results to terminal
            print(f"Results for input_type: `{input_type}`")
            print("Algorithm\tSize\tTime(s)\tComparisons")
            for alg in algorithms:
                name = alg.__name__
                for s, t, c in zip(series[name]["sizes"], series[name]["time"], series[name]["comparisons"]):
                    print(f"{name}\t{s}\t{t:.6f}\t{int(c)}")

            # Plot results
            if show_plot:
                fig, (ax_time, ax_comp) = plt.subplots(1, 2, figsize=(12, 5))
                for alg in algorithms:
                    name = alg.__name__
                    ax_time.plot(series[name]["sizes"], series[name]["time"], marker="o", label=name)
                    ax_comp.plot(series[name]["sizes"], series[name]["comparisons"], marker="o", label=name)

                ax_time.set_title(f"Time vs Size ({input_type})")
                ax_time.set_xlabel("Size")
                ax_time.set_ylabel("Time (s)")
                ax_time.legend()
                ax_comp.set_title(f"Comparisons vs Size ({input_type})")
                ax_comp.set_xlabel("Size")
                ax_comp.set_ylabel("Comparisons")
                ax_comp.legend()
                plt.tight_layout()
                plt.show()


def generate_input(size, input_type):
    if input_type == "random":
        return [random.randint(0, size*10) for _ in range(size)]
    elif input_type == "sorted":
        return list(range(size))
    elif input_type == "reverse":
        return list(range(size, 0, -1))
    elif input_type == "almost_sorted":
        arr = list(range(size))
        # swap 5% of elements
        for _ in range(size // 20):
            i, j = random.sample(range(size), 2)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif input_type == "duplicates":
        return [random.randint(0, 10) for _ in range(size)]
    return None