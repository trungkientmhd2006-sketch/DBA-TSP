
"""Nearest Neighbor heuristic for the Traveling Salesman Problem."""

from collections.abc import Sequence


def nearest_neighbor(
    distances: Sequence[Sequence[float]],
    start_city: int = 0,
) -> tuple[list[int], float]:
    """Build a TSP tour using the Nearest Neighbor heuristic."""

    number_of_cities = len(distances)

    if number_of_cities < 2:
        raise ValueError("At least two cities are required.")

    if any(len(row) != number_of_cities for row in distances):
        raise ValueError("Distance matrix must be square.")

    if type(start_city) is not int or not (0 <= start_city < number_of_cities):
        raise ValueError("Invalid starting city.")

    unvisited = set(range(number_of_cities))
    unvisited.remove(start_city)

    tour = [start_city]
    current_city = start_city

    while unvisited:
        next_city = min(
            unvisited,
            key=lambda city: distances[current_city][city],
        )

        tour.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city

    total_distance = sum(
        distances[tour[i]][tour[i + 1]]
        for i in range(number_of_cities - 1)
    )

    total_distance += distances[tour[-1]][tour[0]]

    return tour, total_distance


def multi_start_nearest_neighbor(
    distances: Sequence[Sequence[float]],
) -> tuple[list[int], float]:
    """Run Nearest Neighbor from every city and return the best tour."""

    number_of_cities = len(distances)

    if number_of_cities < 2:
        raise ValueError("At least two cities are required.")

    best_tour = None
    best_cost = float("inf")

    for start_city in range(number_of_cities):
        tour, cost = nearest_neighbor(
            distances,
            start_city=start_city,
        )

        if cost < best_cost:
            best_tour = tour
            best_cost = cost

    return best_tour, best_cost
