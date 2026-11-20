
"""Repeated-run experiments and summary statistics."""

import csv
from pathlib import Path
import math
import random
import statistics
import time
from collections.abc import Sequence

from src.dba import solve_tsp


def run_experiments(
    distances: Sequence[Sequence[float]],
    seeds: Sequence[int] = tuple(range(10)),
    population_size: int = 50,
    iterations: int = 50,
) -> dict:
    """Run DBA repeatedly and calculate summary statistics."""

    if not seeds:
        raise ValueError("At least one random seed is required.")

    if any(type(seed) is not int for seed in seeds):
        raise ValueError("All seeds must be integers.")

    if len(set(seeds)) != len(seeds):
        raise ValueError("Seeds must be unique.")

    if type(population_size) is not int or population_size < 1:
        raise ValueError("Population size must be at least 1.")

    if type(iterations) is not int or iterations < 1:
        raise ValueError("Iterations must be at least 1.")

    results = []

    # Run DBA with each random seed.
    for seed in seeds:
        start_time = time.perf_counter()

        result = solve_tsp(
            distances,
            population_size=population_size,
            iterations=iterations,
            seed=seed,
        )

        runtime = time.perf_counter() - start_time

        results.append({
            "seed": seed,
            "best_cost": result["best_cost"],
            "best_tour": result["best_tour"],
            "runtime": runtime,
            "history": result["history"],
        })

    # Extract best costs and runtimes.
    costs = [result["best_cost"] for result in results]
    runtimes = [result["runtime"] for result in results]

    # Calculate summary statistics.
    summary = {
        "number_of_runs": len(results),
        "population_size": population_size,
        "iterations": iterations,
        "best": min(costs),
        "worst": max(costs),
        "mean": statistics.mean(costs),
        "std": statistics.stdev(costs) if len(costs) > 1 else 0.0,
        "mean_runtime": statistics.mean(runtimes),
        "total_runtime": sum(runtimes),
    }

    return {
        "results": results,
        "summary": summary,
    }



def save_experiment_results(
    experiment: dict,
    instance_name: str = "eil51",
    output_dir: str = "data/results",
) -> None:
    """Save individual runs and summary statistics to CSV files."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Save individual run results.
    runs_file = output_path / f"dba_{instance_name}_runs.csv"

    with runs_file.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "seed",
                "best_cost",
                "runtime",
                "best_tour",
            ],
        )

        writer.writeheader()

        for result in experiment["results"]:
            writer.writerow({
                "seed": result["seed"],
                "best_cost": result["best_cost"],
                "runtime": result["runtime"],
                "best_tour": " ".join(
                    map(str, result["best_tour"])
                ),
            })

    # Save summary statistics.
    summary_file = output_path / f"dba_{instance_name}_summary.csv"

    with summary_file.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Metric", "Value"])

        for key, value in experiment["summary"].items():
            writer.writerow([key, value])

    print("Results saved successfully:")
    print(runs_file)
    print(summary_file)
