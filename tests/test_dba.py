
import random

import pytest

from src.bat import Bat
from src.dba import (
    initialize_population,
    calculate_velocity,
    move_bat,
    local_search,
    accept_solution,
    update_bat_parameters,
    solve_tsp,
    calculate_two_opt_delta,
)
from src.problem import read_tsplib, calculate_distance_matrix, is_valid_tour


@pytest.fixture
def distances():
    cities = read_tsplib("data/instances/eil51.tsp")
    return calculate_distance_matrix(cities)


def test_initialize_population(distances):
    population = initialize_population(distances, population_size=10, seed=42)

    assert len(population) == 10
    assert all(is_valid_tour(bat.tour, len(distances)) for bat in population)


def test_calculate_velocity():
    rng = random.Random(42)

    velocity = calculate_velocity(
        [0, 1, 2, 3],
        [1, 0, 3, 2],
        rng,
    )

    assert 1 <= velocity <= 4


def test_move_bat(distances):
    population = initialize_population(distances, seed=42)
    bat = population[0]

    new_tour, new_cost = move_bat(
        bat.tour,
        distances,
        5,
        random.Random(42),
    )

    assert is_valid_tour(new_tour, len(distances))
    assert new_cost <= bat.cost


def test_local_search(distances):
    population = initialize_population(distances, seed=42)

    new_tour, new_cost = local_search(
        population,
        distances,
        random.Random(42),
    )

    assert is_valid_tour(new_tour, len(distances))
    assert new_cost <= min(bat.cost for bat in population)


def test_accept_solution():
    assert accept_solution(100, 90, 1.0, random.Random(42))
    assert not accept_solution(90, 100, 1.0, random.Random(42))
    assert not accept_solution(100, 100, 1.0, random.Random(42))


def test_update_bat_parameters():
    bat = Bat(
        tour=[0, 1, 2, 3],
        cost=100,
        loudness=0.8,
        pulse_rate=0.2,
        initial_pulse_rate=0.2,
    )

    update_bat_parameters(bat, 10)

    assert bat.loudness == pytest.approx(0.784)
    assert bat.pulse_rate > 0.19
    assert bat.pulse_rate <= bat.initial_pulse_rate


def test_solve_tsp(distances):
    result = solve_tsp(
        distances,
        population_size=5,
        iterations=3,
        seed=42,
    )

    assert is_valid_tour(result["best_tour"], len(distances))
    assert len(result["history"]) == 4
    assert result["history"][-1] == result["best_cost"]
    assert result["history"][-1] <= result["history"][0]


def test_calculate_two_opt_delta(distances):
    from src.operators import two_opt
    from src.problem import tour_length

    tour = list(range(len(distances)))
    random.Random(42).shuffle(tour)

    original_cost = tour_length(tour, distances)

    for i in range(len(tour) - 1):
        for j in range(i + 1, len(tour)):
            new_tour = two_opt(tour, i, j)

            expected_delta = (
                tour_length(new_tour, distances) - original_cost
            )

            actual_delta = calculate_two_opt_delta(
                tour,
                distances,
                i,
                j,
            )

            assert actual_delta == expected_delta