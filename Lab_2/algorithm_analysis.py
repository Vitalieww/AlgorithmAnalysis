import random
import time


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
        # Wrap input values in Comparable objects
        arr = [Comparable(v, counter) for v in input_data]

        start_time = time.perf_counter()
        algorithm(arr)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        comparisons = counter.count

        self.results.append({
            "algorithm": algorithm.__name__,
            "input_type": input_type,
            "size": size,
            "time": elapsed_time,
            "comparisons": comparisons
        })


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