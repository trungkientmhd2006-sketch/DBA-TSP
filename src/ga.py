
"""Genetic Algorithm for the Traveling Salesman Problem."""

import random
from collections.abc import Sequence

from src.problem import tour_length
from src.operators import swap, insertion, two_opt


def order_crossover(
    parent1: Sequence[int],
    parent2: Sequence[int],
    rng: random.Random,
) -> list[int]:
    """Create one valid offspring using Order Crossover (OX)."""

    if len(parent1) != len(parent2):
        raise ValueError("Parents must have the same length.")

    n = len(parent1)

    if n < 2 or set(parent1) != set(parent2):
        raise ValueError("Parents must contain the same cities.")

    start, end = sorted(rng.sample(range(n), 2))

    child = [None] * n
    child[start:end + 1] = parent1[start:end + 1]

    remaining = [
        city
        for city in parent2
        if city not in child
    ]

    position = (end + 1) % n

    for city in remaining:
        while child[position] is not None:
            position = (position + 1) % n

        child[position] = city
        position = (position + 1) % n

    return child


def tournament_selection(
    population: list[list[int]],
    costs: list[float],
    tournament_size: int,
    rng: random.Random,
) -> list[int]:
    """Select the best individual from a random tournament."""

    candidates = rng.sample(
        range(len(population)),
        tournament_size,
    )

    winner = min(candidates, key=lambda i: costs[i])

    return population[winner][:]


def mutate_tour(
    tour: Sequence[int],
    rng: random.Random,
) -> list[int]:
    """Apply one randomly selected permutation mutation."""

    n = len(tour)
    i, j = sorted(rng.sample(range(n), 2))

    mutation = rng.choice(["swap", "insertion", "inversion"])

    if mutation == "swap":
        return swap(tour, i, j)

    if mutation == "insertion":
        return insertion(tour, i, j)

    return two_opt(tour, i, j)


def solve_tsp_ga(
    distances: Sequence[Sequence[float]],
    population_size: int = 50,
    generations: int = 50,
    crossover_rate: float = 0.9,
    mutation_rate: float = 0.2,
    tournament_size: int = 3,
    elite_size: int = 1,
    seed: int | None = None,
) -> dict:
    """Solve TSP using a Genetic Algorithm."""

    if population_size < 2:
        raise ValueError("Population size must be at least 2.")

    if generations < 1:
        raise ValueError("Generations must be at least 1.")

    if not 0 <= crossover_rate <= 1:
        raise ValueError("Crossover rate must be between 0 and 1.")

    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1.")

    if not 1 <= tournament_size <= population_size:
        raise ValueError("Invalid tournament size.")

    if not 1 <= elite_size < population_size:
        raise ValueError("Elite size must be between 1 and population_size - 1.")

    rng = random.Random(seed)
    n = len(distances)

    if n < 2:
        raise ValueError("At least two cities are required.")

    # Initialize population with random permutations.
    population = []

    for _ in range(population_size):
        tour = list(range(n))
        rng.shuffle(tour)
        population.append(tour)

    costs = [
        tour_length(tour, distances)
        for tour in population
    ]

    best_index = min(range(population_size), key=lambda i: costs[i])
    best_tour = population[best_index][:]
    best_cost = costs[best_index]

    history = [best_cost]

    # Evolution process.
    for _ in range(generations):

        # Sort individuals by their costs.
        ranked_indices = sorted(
            range(population_size),
            key=lambda i: costs[i],
        )

        # Elitism: preserve the best individuals.
        new_population = [
            population[i][:]
            for i in ranked_indices[:elite_size]
        ]

        while len(new_population) < population_size:

            parent1 = tournament_selection(
                population,
                costs,
                tournament_size,
                rng,
            )

            parent2 = tournament_selection(
                population,
                costs,
                tournament_size,
                rng,
            )

            # Crossover.
            if rng.random() < crossover_rate:
                child = order_crossover(parent1, parent2, rng)
            else:
                child = parent1[:]

            # Mutation.
            if rng.random() < mutation_rate:
                child = mutate_tour(child, rng)

            new_population.append(child)

        population = new_population

        costs = [
            tour_length(tour, distances)
            for tour in population
        ]

        generation_best = min(range(population_size), key=lambda i: costs[i])

        if costs[generation_best] < best_cost:
            best_cost = costs[generation_best]
            best_tour = population[generation_best][:]

        history.append(best_cost)

    return {
        "best_tour": best_tour,
        "best_cost": best_cost,
        "history": history,
    }
