import time
import matplotlib.pyplot as plt

class EmpiricalTest:
    def __init__(self, fib_function, name=None):
        """
        fib_function: callable taking an int n and returning fib(n)
        name: optional name for display purposes
        """
        self.fib_function = fib_function
        self.name = name or fib_function.__name__

    def _measure_time(self, n, repetitions):
        """
        Measure average execution time for fib(n)
        """
        times = []

        for _ in range(repetitions):
            start = time.perf_counter()
            self.fib_function(n)
            end = time.perf_counter()
            times.append(end - start)

        return sum(times) / len(times)

    def run(self, n_values, repetitions=1):
        """
        Run empirical test for all n in n_values

        Returns:
            dict: { n : average_execution_time }
        """
        results = {}

        for n in n_values:
            avg_time = self._measure_time(n, repetitions)
            results[n] = avg_time

        return results

    def print_results(self, results):
        """
        Print results to terminal
        """
        print(f"\nEmpirical results for: {self.name}")
        print("-" * 40)

        for n, time_taken in results.items():
            print(f"n = {n:<5} | time = {time_taken:.6f} s")

    def plot_results(self, results):
        """
        Plot execution time vs n
        """
        n_values = list(results.keys())
        times = list(results.values())


        plt.xlabel("n-th Fibonacci Term")
        plt.ylabel("Execution time (s)")
        plt.plot(n_values, times, marker='o', linestyle='-', label=self.name)
        plt.locator_params(axis='x', integer=True)
        plt.title(self.name + " Function")
        plt.show()

    def overall_test(self, n_values, repetitions=1):
        """
        Run the overall test: measure, print, and plot results
        """
        results = self.run(n_values, repetitions)
        self.print_results(results)
        self.plot_results(results)


class MultiEmpiricalTest:
    def __init__(self, fib_functions):
        """
        fib_functions: iterable of either
            - a callable (name inferred from callable.__name__)
            - a (callable, name) tuple to override the display name
        """
        self.tests = []
        for item in fib_functions:
            if isinstance(item, (list, tuple)):
                func, name = item[0], item[1]
            else:
                func, name = item, None
            self.tests.append(EmpiricalTest(func, name))

    def run_all(self, n_values, repetitions=1):
        """
        Measure execution times for all registered tests.
        Returns dict: { test_name: { n: avg_time, ... }, ... }
        """
        results = {}
        for test in self.tests:
            results[test.name] = test.run(n_values, repetitions)
        return results

    def print_all(self, results):
        """
        Print results for all tests. `results` should be the dict returned by run_all.
        """
        for test in self.tests:
            res = results.get(test.name, {})
            test.print_results(res)

    def plot_all(self, results):
        """
        Plot all methods on a single graph. `results` should be the dict returned by run_all.
        """
        import itertools
        markers = ['o', 's', 'D', '^', 'v', '<', '>', 'P', 'X', '*']
        marker_cycle = itertools.cycle(markers)

        plt.figure(figsize=(8, 5))
        for test in self.tests:
            res = results.get(test.name, {})
            if not res:
                continue
            n_values = sorted(res.keys())
            times = [res[n] for n in n_values]
            plt.plot(n_values, times, marker=next(marker_cycle), linestyle='-', label=test.name)

        plt.xlabel("n-th Fibonacci Term")
        plt.ylabel("Execution time (s)")
        plt.title("Fibonacci Methods Comparison")
        plt.locator_params(axis='x', integer=True)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def overall_test(self, n_values, repetitions=1):
        """
        Run measurement, print results, and plot comparison.
        """
        results = self.run_all(n_values, repetitions)
        self.print_all(results)
        self.plot_all(results)