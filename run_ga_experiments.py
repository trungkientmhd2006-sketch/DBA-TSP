
import csv
import statistics
import time
from pathlib import Path

from src.problem import (
    read_tsplib,
    calculate_distance_matrix,
    is_valid_tour,
    tour_length,
)
from src.ga import solve_tsp_ga


def main():
    # Load EIL51 dataset.
    coordinates = read_tsplib("data/instances/eil51.tsp")
    distances = calculate_distance_matrix(coordinates)

    results = []

    # Run GA with seeds 0 to 9.
    for seed in range(10):
        start_time = time.perf_counter()

        result = solve_tsp_ga(
            distances,
            population_size=50,
            generations=50,
            seed=seed,
        )

        runtime = time.perf_counter() - start_time

        # Validate the returned solution.
        assert is_valid_tour(result["best_tour"], len(coordinates))
        assert result["best_cost"] == tour_length(
            result["best_tour"], distances
        )

        results.append({
            "seed": seed,
            "best_cost": result["best_cost"],
            "runtime": runtime,
            "best_tour": result["best_tour"],
        })

    costs = [result["best_cost"] for result in results]
    runtimes = [result["runtime"] for result in results]

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

    # Create output directory.
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save individual runs.
    runs_path = output_dir / "ga_eil51_runs.csv"

    with runs_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
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

        for result in results:
            writer.writerow({
                **result,
                "best_tour": " ".join(
                    map(str, result["best_tour"])
                ),
            })

    # Save summary statistics.
    summary_path = output_dir / "ga_eil51_summary.csv"

    with summary_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["Metric", "Value"])
        writer.writerows(summary.items())

    # Display results.
    print("\nGA RESULTS ON EIL51")
    print("-" * 40)
    print("Seed | Best Cost | Runtime (seconds)")

    for result in results:
        print(
            result["seed"],
            "|",
            result["best_cost"],
            "|",
            round(result["runtime"], 4),
        )

    print("\nSUMMARY")
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\nAll tours valid: True")
    print("All costs correct: True")
    print(f"Saved: {runs_path}")
    print(f"Saved: {summary_path}")


if __name__ == "__main__":
    main()
