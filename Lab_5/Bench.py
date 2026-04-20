import os
import csv
import time
import argparse
from collections import defaultdict

import matplotlib.pyplot as plt

from GraphGenerator import GraphGenerator
from Kruskal import kruskal
from Prim import prim

OUTPUT_DIR = "bench_results"

def run_experiments(ns, densities, trials=3, seed_base=42, weight_range=(1,100)):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    csv_path = os.path.join(OUTPUT_DIR, "results.csv")
    fieldnames = ["algorithm", "n", "density", "edges", "trial", "time_s", "mst_weight"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for n in ns:
            max_edges = n * (n - 1) // 2
            for density in densities:
                target_e = max(n - 1, min(max_edges, int(round(density * max_edges))))
                for trial in range(trials):
                    seed = seed_base + n + int(density * 1000) + trial
                    gg = GraphGenerator(seed=seed, weight_range=weight_range)
                    gg.generate_connected(n, target_e, seed=seed, weight_range=weight_range)
                    edges = list(gg.edges)

                    # Kruskal
                    t0 = time.perf_counter()
                    mst_k, w_k = kruskal(n, edges)
                    t1 = time.perf_counter()
                    writer.writerow({
                        "algorithm": "kruskal",
                        "n": n,
                        "density": density,
                        "edges": len(edges),
                        "trial": trial,
                        "time_s": t1 - t0,
                        "mst_weight": w_k
                    })

                    # Prim
                    t0 = time.perf_counter()
                    mst_p, w_p = prim(n, edges)
                    t1 = time.perf_counter()
                    writer.writerow({
                        "algorithm": "prim",
                        "n": n,
                        "density": density,
                        "edges": len(edges),
                        "trial": trial,
                        "time_s": t1 - t0,
                        "mst_weight": w_p
                    })

                    # sanity check
                    if w_k != w_p:
                        print(f"Warning: MST weight mismatch n={n} density={density} trial={trial} -> kruskal {w_k} prim {w_p}")

    return csv_path

def plot_results(csv_path):
    rows = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            r["n"] = int(r["n"])
            r["density"] = float(r["density"])
            r["edges"] = int(r["edges"])
            r["time_s"] = float(r["time_s"])
            rows.append(r)

    # aggregate mean time by (algorithm, n, density)
    agg = {}
    for r in rows:
        key = (r["algorithm"], r["n"], r["density"], r["edges"])
        agg.setdefault(key, []).append(r["time_s"])

    points = []
    for (alg, n, density, edges), times in agg.items():
        points.append({"algorithm": alg, "n": n, "density": density, "edges": edges, "time_s": sum(times)/len(times)})

    # runtime vs n (separate curves per algorithm and density)
    plt.figure(figsize=(8,6))
    for density in sorted({p["density"] for p in points}):
        for alg in ("kruskal", "prim"):
            xs = [p["n"] for p in points if p["algorithm"]==alg and p["density"]==density]
            ys = [p["time_s"] for p in points if p["algorithm"]==alg and p["density"]==density]
            if not xs:
                continue
            xs, ys = zip(*sorted(zip(xs, ys)))
            plt.plot(xs, ys, marker='o', label=f"{alg} d={density}")
    plt.xlabel("n (nodes)")
    plt.ylabel("time (s)")
    plt.title("Runtime vs n")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "runtime_vs_n.png"))
    plt.close()

    # runtime vs edges
    plt.figure(figsize=(8,6))
    for alg in ("kruskal", "prim"):
        xs = [p["edges"] for p in points if p["algorithm"]==alg]
        ys = [p["time_s"] for p in points if p["algorithm"]==alg]
        if xs:
            xs, ys = zip(*sorted(zip(xs, ys)))
            plt.plot(xs, ys, marker='o', label=alg)
    plt.xlabel("number of edges")
    plt.ylabel("time (s)")
    plt.title("Runtime vs #edges")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "runtime_vs_edges.png"))
    plt.close()

def print_results_table(csv_path):
    rows = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            r["n"] = int(r["n"])
            r["density"] = float(r["density"])
            r["edges"] = int(r["edges"])
            r["time_s"] = float(r["time_s"])
            rows.append(r)

    agg = {}
    for r in rows:
        key = (r["algorithm"], r["n"], r["density"], r["edges"])
        agg.setdefault(key, []).append(r["time_s"])

    print("\n" + "="*70)
    print(f"{'Algorithm':<12} | {'Nodes (V)':<9} | {'Density':<7} | {'Edges (E)':<9} | {'Avg Time (s)':<15}")
    print("-" * 70)

    # Sort by Nodes, then Density, then Algorithm
    sorted_keys = sorted(agg.keys(), key=lambda x: (x[1], x[2], x[0]))

    for key in sorted_keys:
        alg, n, density, edges = key
        times = agg[key]
        avg_time = sum(times) / len(times)
        print(f"{alg.capitalize():<12} | {n:<9} | {density:<7.2f} | {edges:<9} | {avg_time:.6f}")

    print("="*70 + "\n")

def main():
    # --- USER CONFIGURE HERE ---
    # Choose one of the presets below or replace ns/densities/trials directly.
    # Preset options: "quick", "scale_n", "scale_density", "full"
    preset = "full"

    if preset == "quick":
        ns = [50]                     # small quick smoke test
        densities = [0.5]
        trials = 1
    elif preset == "scale_n":
        ns = [100, 200, 400, 800]     # classic: scale nodes at fixed density
        densities = [0.5]
        trials = 3
    elif preset == "scale_density":
        ns = [200]                    # classic: fix nodes, vary density
        densities = [0.1, 0.3, 0.5, 0.7, 0.9]
        trials = 3
    else:  # "full"
        ns = [100, 200, 400, 800]     # full experiment
        densities = [0.1, 0.5, 0.9]
        trials = 3
    # --- END USER CONFIGURE ---

    print(f"Running benchmark preset={preset} ns={ns} densities={densities} trials={trials}")
    csv_path = run_experiments(ns, densities, trials=trials)
    print_results_table(csv_path)
    plot_results(csv_path)
    print(f"Results written to {csv_path} and plots in {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()