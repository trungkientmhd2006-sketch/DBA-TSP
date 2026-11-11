
"""TSP problem helpers: TSPLIB reader, distance matrix and tour evaluation."""

import math
from pathlib import Path
from collections.abc import Sequence


def is_valid_tour(tour: Sequence[int], n_cities: int) -> bool:
    """Check whether a tour is a permutation of city indices."""
    if n_cities < 2 or len(tour) != n_cities:
        return False

    if any(type(city) is not int for city in tour):
        return False

    return sorted(tour) == list(range(n_cities))


def tour_length(
    tour: Sequence[int],
    distances: Sequence[Sequence[float]]
) -> float:
    """Calculate the total length of a closed TSP tour."""

    n = len(distances)

    if n < 2:
        raise ValueError("A distance matrix must contain at least two cities.")

    if any(len(row) != n for row in distances):
        raise ValueError("The distance matrix must be square.")

    if not is_valid_tour(tour, n):
        raise ValueError("Invalid tour.")

    return sum(
        distances[tour[i]][tour[(i + 1) % n]]
        for i in range(n)
    )


def read_tsplib(filepath: str | Path) -> list[tuple[float, float]]:
    """
    Read a TSPLIB EUC_2D file.

    Returns coordinates in city ID order.
    """

    dimension = None
    edge_weight_type = None
    coordinates = {}
    reading_coordinates = False
    found_eof = False

    with open(filepath, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            if line == "NODE_COORD_SECTION":
                reading_coordinates = True
                continue

            if line == "EOF":
                found_eof = True
                break

            if not reading_coordinates:
                if ":" not in line:
                    continue

                key, value = line.split(":", 1)
                key = key.strip().upper()
                value = value.strip()

                if key == "DIMENSION":
                    dimension = int(value)
                elif key == "EDGE_WEIGHT_TYPE":
                    edge_weight_type = value.upper()

            else:
                parts = line.split()

                if len(parts) != 3:
                    raise ValueError(
                        f"Invalid coordinate at line {line_number}."
                    )

                city_id = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])

                if city_id in coordinates:
                    raise ValueError(f"Duplicate city ID: {city_id}")

                if not math.isfinite(x) or not math.isfinite(y):
                    raise ValueError("City coordinates must be finite.")

                coordinates[city_id] = (x, y)

    if edge_weight_type != "EUC_2D":
        raise ValueError("Only EUC_2D distance type is supported.")

    if dimension is None or dimension < 2:
        raise ValueError("Invalid or missing DIMENSION.")

    if not reading_coordinates:
        raise ValueError("Missing NODE_COORD_SECTION.")

    if not found_eof:
        raise ValueError("Missing EOF marker.")

    if len(coordinates) != dimension:
        raise ValueError("Invalid number of city coordinates.")

    expected_ids = set(range(1, dimension + 1))

    if set(coordinates) != expected_ids:
        raise ValueError("City IDs must be consecutive from 1 to DIMENSION.")

    return [coordinates[i] for i in range(1, dimension + 1)]


def calculate_distance_matrix(
    coordinates: Sequence[tuple[float, float]]
) -> list[list[int]]:
    """Calculate the TSPLIB EUC_2D distance matrix."""

    n = len(coordinates)

    if n < 2:
        raise ValueError("At least two cities are required.")

    for coordinate in coordinates:
        if len(coordinate) != 2:
            raise ValueError("Each city must have exactly two coordinates.")

        x, y = coordinate

        if not math.isfinite(x) or not math.isfinite(y):
            raise ValueError("Coordinates must be finite.")

    distances = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]

            distance = math.sqrt(
                (x1 - x2) ** 2 + (y1 - y2) ** 2
            )

            distance = int(distance + 0.5)

            distances[i][j] = distance
            distances[j][i] = distance

    return distances
