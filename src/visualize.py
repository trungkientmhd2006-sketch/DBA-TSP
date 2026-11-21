
"""Visualization helpers for DBA-TSP."""

import csv
from pathlib import Path
from collections.abc import Sequence

import matplotlib.pyplot as plt


def plot_convergence(
    history: Sequence[float],
    output_path: str = "data/results/convergence_eil51.png",
    show: bool = True,
) -> None:
    """Plot the best-so-far objective value by iteration."""

    if not history:
        raise ValueError("History must not be empty.")

    if any(cost < 0 for cost in history):
        raise ValueError("Costs must be non-negative.")

    iterations = range(len(history))
    best_cost = min(history)

    plt.figure(figsize=(10, 6))

    plt.plot(
        iterations,
        history,
        marker="o",
        markersize=3,
        linewidth=2,
        label="DBA Best Cost",
    )

    plt.axhline(
        y=best_cost,
        linestyle="--",
        linewidth=1.5,
        label=f"Final Best Cost = {best_cost}",
    )

    plt.title("DBA Convergence on eil51")
    plt.xlabel("Iteration")
    plt.ylabel("Best Cost")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Convergence plot saved to: {output_file}")

    if show:
        plt.show()

    plt.close()


def plot_comparison(
    summary_path: str = "data/results/dba_eil51_summary.csv",
    ga_summary_path: str = "data/results/ga_eil51_summary.csv",
    nearest_neighbor_cost: float = 482,
    output_path: str = "data/results/comparison_eil51.png",
    show: bool = True,
) -> None:
    """Compare DBA, GA and Multi-start NN on EIL51."""

    def read_summary(path):
        summary_file = Path(path)

        if not summary_file.exists():
            raise FileNotFoundError(
                f"Summary file not found: {summary_file}"
            )

        with summary_file.open(
            "r",
            newline="",
            encoding="utf-8-sig",
        ) as file:
            reader = csv.DictReader(file)
            return {
                row["Metric"]: float(row["Value"])
                for row in reader
            }

    dba = read_summary(summary_path)
    ga = read_summary(ga_summary_path)

    for name, summary in [("DBA", dba), ("GA", ga)]:
        if "best" not in summary or "mean" not in summary:
            raise ValueError(
                f"{name} summary must contain best and mean."
            )

    labels = [
        "Multi-start NN",
        "DBA Mean",
        "DBA Best",
        "GA Mean",
        "GA Best",
    ]

    costs = [
        nearest_neighbor_cost,
        dba["mean"],
        dba["best"],
        ga["mean"],
        ga["best"],
    ]

    plt.figure(figsize=(10, 6))

    bars = plt.bar(labels, costs, width=0.6)

    plt.title("DBA vs GA vs Multi-start NN on EIL51")
    plt.xlabel("Algorithm")
    plt.ylabel("Tour Cost")
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.xticks(rotation=10)

    for bar, cost in zip(bars, costs):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 3,
            f"{cost:.1f}",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Comparison plot saved to: {output_file}")

    if show:
        plt.show()

    plt.close()
