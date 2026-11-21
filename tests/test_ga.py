
import random

import pytest

from src.ga import (
    order_crossover,
    mutate_tour,
    solve_tsp_ga,
)
from src.problem import (
    calculate_distance_matrix,
    is_valid_tour,
    tour_length,
)


@pytest.fixture
def distances():
    coordinates = [
        (0, 0),
        (10, 0),
        (10, 10),
        (0, 10),
        (5, 5),
    ]
    return calculate_distance_matrix(coordinates)


def test_order_crossover_preserves_permutation():
    parent1 = [0, 1, 2, 3, 4]
    parent2 = [4, 3, 2, 1, 0]

    child = order_crossover(
        parent1,
        parent2,
        random.Random(42),
    )

    assert len(child) == len(parent1)
    assert sorted(child) == sorted(parent1)


def test_order_crossover_does_not_modify_parents():
    parent1 = [0, 1, 2, 3, 4]
    parent2 = [4, 3, 2, 1, 0]

    original1 = parent1[:]
    original2 = parent2[:]

    order_crossover(parent1, parent2, random.Random(42))

    assert parent1 == original1
    assert parent2 == original2


@pytest.mark.parametrize(
    "mutation_name",
    ["swap", "insertion", "inversion"],
)
def test_mutation_preserves_permutation(mutation_name):
    tour = [0, 1, 2, 3, 4]

    result = mutate_tour(tour, random.Random(42))

    assert len(result) == len(tour)
    assert sorted(result) == sorted(tour)
    assert tour == [0, 1, 2, 3, 4]


def test_ga_returns_valid_tour(distances):
    result = solve_tsp_ga(
        distances,
        population_size=20,
        generations=30,
        seed=42,
    )

    assert is_valid_tour(result["best_tour"], 5)


def test_ga_cost_is_correct(distances):
    result = solve_tsp_ga(
        distances,
        population_size=20,
        generations=30,
        seed=42,
    )

    actual_cost = tour_length(result["best_tour"], distances)

    assert result["best_cost"] == actual_cost


def test_ga_history_is_non_increasing(distances):
    result = solve_tsp_ga(
        distances,
        population_size=20,
        generations=30,
        seed=42,
    )

    history = result["history"]

    assert len(history) == 31
    assert all(
        history[i] <= history[i - 1]
        for i in range(1, len(history))
    )


def test_ga_is_reproducible(distances):
    result1 = solve_tsp_ga(
        distances,
        population_size=20,
        generations=30,
        seed=42,
    )

    result2 = solve_tsp_ga(
        distances,
        population_size=20,
        generations=30,
        seed=42,
    )

    assert result1["best_tour"] == result2["best_tour"]
    assert result1["best_cost"] == result2["best_cost"]


def test_ga_rejects_invalid_population_size(distances):
    with pytest.raises(ValueError):
        solve_tsp_ga(distances, population_size=1)


def test_ga_rejects_invalid_generations(distances):
    with pytest.raises(ValueError):
        solve_tsp_ga(distances, generations=0)
