
"""Run DBA, GA and Multi-start NN experiments on Berlin52."""

import csv
import statistics
import time
from pathlib import Path

from src.problem import read_tsplib, calculate_distance_matrix
from src.experiment import run_experiments, save_experiment_results
from src.ga import solve_tsp_ga
from src.nearest_neighbor import multi_start_nearest_neighbor


DATA_FILE = "data/instances/berlin52.tsp"
OUTPUT_DIR = Path("data/results")
SEEDS = range(10)

POPULATION_SIZE = 50
ITERATIONS = 50


def run_ga_experiments(distances):
    """Run GA 10 times and calculate summary statistics."""

    results = []

    for seed in SEEDS:
        start = time.perf_counter()

        result = solve_tsp_ga(
            distances,
            population_size=50,
            generations=50,
            crossover_rate=0.9,
            mutation_rate=0.2,
            tournament_size=3,
            elite_size=1,
            seed=seed,
        )

        runtime = time.perf_counter() - start

        results.append({
            "seed": seed,
            "best_cost": result["best_cost"],
            "best_tour": result["best_tour"],
            "runtime": runtime,
        })

        print(
            f"GA seed {seed}: "
            f"cost={result['best_cost']}, "
            f"time={runtime:.4f}s"
        )

    costs = [r["best_cost"] for r in results]
    runtimes = [r["runtime"] for r in results]

    summary = {
        "number_of_runs": len(results),
        "population_size": 50,
        "generations": 50,
        "best": min(costs),
        "worst": max(costs),
        "mean": statistics.mean(costs),
        "std": statistics.stdev(costs),
        "mean_runtime": statistics.mean(runtimes),
        "total_runtime": sum(runtimes),
    }

    return {"results": results, "summary": summary}


def save_ga_results(experiment):
    """Save GA individual runs and summary."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    runs_path = OUTPUT_DIR / "ga_berlin52_runs.csv"

    with runs_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["seed", "best_cost", "runtime", "best_tour"],
        )
        writer.writeheader()

        for result in experiment["results"]:
            writer.writerow({
                "seed": result["seed"],
                "best_cost": result["best_cost"],
                "runtime": result["runtime"],
                "best_tour": " ".join(map(str, result["best_tour"])),
            })

    summary_path = OUTPUT_DIR / "ga_berlin52_summary.csv"

    with summary_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Metric", "Value"])

        for key, value in experiment["summary"].items():
            writer.writerow([key, value])

    print("GA results saved:", runs_path, summary_path)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Read Berlin52.
    coordinates = read_tsplib(DATA_FILE)
    distances = calculate_distance_matrix(coordinates)

    print("Dataset: Berlin52")
    print("Number of cities:", len(coordinates))
    print("Matrix size:", len(distances), "x", len(distances[0]))

    # 2. Run DBA.
    print("\n===== DBA: 10 RUNS =====")

    dba_experiment = run_experiments(
        distances,
        seeds=SEEDS,
        population_size=POPULATION_SIZE,
        iterations=ITERATIONS,
    )

    save_experiment_results(
        dba_experiment,
        instance_name="berlin52",
    )

    print("DBA summary:", dba_experiment["summary"])

    # 3. Run GA.
    print("\n===== GA: 10 RUNS =====")

    ga_experiment = run_ga_experiments(distances)
    save_ga_results(ga_experiment)

    print("GA summary:", ga_experiment["summary"])

    # 4. Run Multi-start Nearest Neighbor.
    print("\n===== MULTI-START NN =====")

    start = time.perf_counter()
    nn_tour, nn_cost = multi_start_nearest_neighbor(distances)
    nn_runtime = time.perf_counter() - start

    print("NN best cost:", nn_cost)
    print("NN runtime:", f"{nn_runtime:.6f}s")

    nn_path = OUTPUT_DIR / "nn_berlin52_summary.csv"

    with nn_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["best_cost", nn_cost])
        writer.writerow(["runtime", nn_runtime])
        writer.writerow(["best_tour", " ".join(map(str, nn_tour))])

    print("\n===== EXPERIMENT COMPLETED =====")
    print("Results directory:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
