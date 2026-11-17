"""Discrete Bat Algorithm for the Traveling Salesman Problem."""

import math
import random
from collections.abc import Sequence

from src.bat import Bat
from src.operators import hamming_distance, two_opt
from src.problem import tour_length


def initialize_population(
    distances: Sequence[Sequence[float]],
    population_size: int = 50,
    seed: int | None = None,
) -> list[Bat]:
    """Create a random initial population of bats."""

    if population_size < 1:
        raise ValueError("Population size must be at least 1.")

    number_of_cities = len(distances)

    if number_of_cities < 3:
        raise ValueError("TSP must contain at least 3 cities.")

    rng = random.Random(seed)
    population = []

    for _ in range(population_size):
        # Generate a random permutation of all cities.
        tour = rng.sample(range(number_of_cities), number_of_cities)

        # Calculate the cost of this tour.
        cost = tour_length(tour, distances)

        # Initialize loudness and pulse rate according to the paper.
        loudness = rng.uniform(0.7, 1.0)
        initial_pulse_rate = rng.uniform(0.0, 0.4)

        bat = Bat(
            tour=tour,
            cost=cost,
            velocity=1,
            loudness=loudness,
            pulse_rate=initial_pulse_rate,
            initial_pulse_rate=initial_pulse_rate,
        )

        population.append(bat)

    return population



def solve_tsp(
    distances: Sequence[Sequence[float]],
    population_size: int = 50,
    iterations: int = 1000,
    seed: int | None = None,
) -> dict:
    """Optimize a TSP tour using the discrete bat algorithm."""

    if iterations < 1:
        raise ValueError("Iterations must be at least 1.")

    rng = random.Random(seed)

    # Step 1: Initialize the population.
    population = initialize_population(
        distances,
        population_size=population_size,
        seed=seed,
    )

    # Step 2: Find the initial global best solution.
    best_bat = min(population, key=lambda bat: bat.cost)
    best_tour = best_bat.tour.copy()
    best_cost = best_bat.cost

    # Store the best cost after each iteration.
    history = [best_cost]

    alpha = 0.98
    gamma = 0.98

    # Step 3: Main DBA loop.
    for iteration in range(1, iterations + 1):

        for bat in population:

            # Step 4: Calculate discrete velocity.
            bat.velocity = calculate_velocity(
                bat.tour,
                best_tour,
                rng,
            )

            # Step 5: Move the bat using 2-opt.
            new_tour, new_cost = move_bat(
                bat.tour,
                distances,
                bat.velocity,
                rng,
            )

            # Step 6: Local search when rand > pulse rate.
            if rng.random() > bat.pulse_rate:
                local_tour, local_cost = local_search(
                    population,
                    distances,
                    rng,
                )

                if local_cost < new_cost:
                    new_tour = local_tour
                    new_cost = local_cost

            # Step 7: Accept the new solution.
            if accept_solution(
                bat.cost,
                new_cost,
                bat.loudness,
                rng,
            ):
                bat.tour = new_tour
                bat.cost = new_cost

            # Step 8: Update the global best.
            if bat.cost < best_cost:
                best_tour = bat.tour.copy()
                best_cost = bat.cost

            # Step 9: Update loudness and pulse rate.
            update_bat_parameters(
                bat,
                iteration,
                alpha=alpha,
                gamma=gamma,
            )

        history.append(best_cost)

    return {
        "best_tour": best_tour,
        "best_cost": best_cost,
        "history": history,
        "iterations": iterations,
    }






def calculate_velocity(
    tour: Sequence[int],
    best_tour: Sequence[int],
    rng: random.Random,
) -> int:
    """Calculate discrete velocity using Hamming distance."""

    distance = hamming_distance(tour, best_tour)

    # The bat already has the same tour as the global best.
    if distance == 0:
        return 0

    return rng.randint(1, distance)



def move_bat(
    tour: Sequence[int],
    distances: Sequence[Sequence[float]],
    velocity: int,
    rng: random.Random,
) -> tuple[list[int], float]:
    """Generate velocity 2-opt neighbors and select the best one."""

    if type(velocity) is not int or velocity < 0:
        raise ValueError("Velocity must be a non-negative integer.")

    best_tour = list(tour)
    best_cost = tour_length(best_tour, distances)

    if velocity == 0:
        return best_tour, best_cost

    number_of_cities = len(tour)

    if number_of_cities < 3:
        raise ValueError("A 2-opt move requires at least 3 cities.")

    for _ in range(velocity):
        # Randomly select two different positions.
        i, j = sorted(rng.sample(range(number_of_cities), 2))

        # Generate one 2-opt neighbor from the original tour.
        candidate = two_opt(tour, i, j)
        candidate_cost = tour_length(candidate, distances)

        # Keep the best neighbor.
        if candidate_cost < best_cost:
            best_tour = candidate
            best_cost = candidate_cost

    return best_tour, best_cost



def local_search(
    population: Sequence[Bat],
    distances: Sequence[Sequence[float]],
    rng: random.Random,
) -> tuple[list[int], float]:
    """Find the best 2-opt neighbor around a randomly selected top bat."""

    if not population:
        raise ValueError("Population must not be empty.")

    top_bats = sorted(population, key=lambda bat: bat.cost)[:10]
    selected_bat = rng.choice(top_bats)

    best_tour = list(selected_bat.tour)
    best_cost = selected_bat.cost

    number_of_cities = len(best_tour)

    for i in range(number_of_cities - 1):
        for j in range(i + 1, number_of_cities):

            delta = calculate_two_opt_delta(
                selected_bat.tour,
                distances,
                i,
                j,
            )

            candidate_cost = selected_bat.cost + delta

            if candidate_cost < best_cost:
                best_tour = two_opt(selected_bat.tour, i, j)
                best_cost = candidate_cost

    return best_tour, best_cost


def accept_solution(
    old_cost: float,
    new_cost: float,
    loudness: float,
    rng: random.Random,
) -> bool:
    """Decide whether a bat accepts a new solution."""

    return (
        rng.random() < loudness
        and new_cost < old_cost
    )


import math


def update_bat_parameters(
    bat: Bat,
    iteration: int,
    alpha: float = 0.98,
    gamma: float = 0.98,
) -> None:
    """Update loudness and pulse rate of a bat."""

    bat.loudness *= alpha

    bat.pulse_rate = bat.initial_pulse_rate * (
        1 - math.exp(-gamma * iteration)
    )




def calculate_two_opt_delta(
    tour: Sequence[int],
    distances: Sequence[Sequence[float]],
    i: int,
    j: int,
) -> float:
    """Calculate the cost change of a 2-opt move for symmetric TSP."""

    n = len(tour)
        # Reversing the entire tour does not change its cost.
    if i == 0 and j == n - 1:
        return 0

    a = tour[i - 1]
    b = tour[i]
    c = tour[j]
    d = tour[(j + 1) % n]

    old_cost = distances[a][b] + distances[c][d]
    new_cost = distances[a][c] + distances[b][d]

    return new_cost - old_cost
