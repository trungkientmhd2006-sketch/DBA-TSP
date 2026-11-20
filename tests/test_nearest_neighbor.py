
import pytest

from src.nearest_neighbor import (
    nearest_neighbor,
    multi_start_nearest_neighbor,
)
from src.problem import (
    read_tsplib,
    calculate_distance_matrix,
    is_valid_tour,
    tour_length,
)


@pytest.fixture
def distances():
    cities = read_tsplib("data/instances/eil51.tsp")
    return calculate_distance_matrix(cities)


def test_nearest_neighbor_returns_valid_tour(distances):
    tour, cost = nearest_neighbor(distances)

    assert len(tour) == len(distances)
    assert is_valid_tour(tour, len(distances))
    assert cost > 0


def test_nearest_neighbor_respects_start_city(distances):
    tour, cost = nearest_neighbor(distances, start_city=10)

    assert tour[0] == 10
    assert is_valid_tour(tour, len(distances))


def test_nearest_neighbor_cost_is_correct(distances):
    tour, cost = nearest_neighbor(distances)

    expected_cost = tour_length(tour, distances)

    assert cost == expected_cost


def test_nearest_neighbor_rejects_invalid_start_city(distances):
    with pytest.raises(ValueError):
        nearest_neighbor(distances, start_city=100)


def test_nearest_neighbor_rejects_small_matrix():
    with pytest.raises(ValueError):
        nearest_neighbor([[0]])


def test_nearest_neighbor_rejects_non_square_matrix():
    distances = [
        [0, 10],
        [10, 0],
        [5, 8],
    ]

    with pytest.raises(ValueError):
        nearest_neighbor(distances)

def test_multi_start_returns_valid_tour(distances):
    tour, cost = multi_start_nearest_neighbor(distances)

    assert is_valid_tour(tour, len(distances))
    assert cost == tour_length(tour, distances)


def test_multi_start_returns_best_starting_city(distances):
    _, best_cost = multi_start_nearest_neighbor(distances)

    all_costs = [
        nearest_neighbor(distances, start_city=i)[1]
        for i in range(len(distances))
    ]

    assert best_cost == min(all_costs)