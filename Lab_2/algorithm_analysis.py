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
        if isinstance(input_types, str):
            input_types = [input_types]

        for input_type in input_types:
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

            self._print_table(series, input_type)

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

    def _print_table(self, series, input_type):
        headers = ["Algorithm", "Size", "Time (s)", "Comparisons"]
        rows = []
        for name, data in series.items():
            for s, t, c in zip(data["sizes"], data["time"], data["comparisons"]):
                rows.append([name, str(s), f"{t:.6f}", str(int(c))])

        # compute column widths
        cols = list(zip(*([headers] + rows))) if rows else [(h,) for h in headers]
        col_widths = [max(len(cell) for cell in col) for col in cols]

        def fmt_row(row):
            return "| " + " | ".join(cell.ljust(w) for cell, w in zip(row, col_widths)) + " |"

        sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"

        print(f"Results for input_type: `{input_type}`")
        print(sep)
        print(fmt_row(headers))
        print(sep)
        for r in rows:
            print(fmt_row(r))
        print(sep)

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