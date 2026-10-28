"""TSP model helpers. Implement and test these before the DBA loop."""

from collections.abc import Sequence


def tour_length(tour: Sequence[int], distances: Sequence[Sequence[float]]) -> float:
    """Return the closed-tour cost, including the edge back to the start."""
    if len(tour) < 2:
        raise ValueError("A tour must contain at least two cities.")
    return sum(
        distances[tour[i]][tour[(i + 1) % len(tour)]]
        for i in range(len(tour))
    )


def is_valid_tour(tour: Sequence[int], n_cities: int) -> bool:
    """Return True when tour is a permutation of city indices 0..n_cities-1."""
    return len(tour) == n_cities and sorted(tour) == list(range(n_cities))
