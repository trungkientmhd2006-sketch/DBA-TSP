"""Discrete permutation operators for DBA/IBA."""

from collections.abc import Sequence


def hamming_distance(a: Sequence[int], b: Sequence[int]) -> int:
    """Count positions at which two same-length tours differ."""
    if len(a) != len(b):
        raise ValueError("Tours must have the same length.")

    return sum(x != y for x, y in zip(a, b))


def swap(tour: Sequence[int], i: int, j: int) -> list[int]:
    """
    Exchange the elements at positions i and j.

    Return a new list without modifying the original tour.
    """
    if type(i) is not int or type(j) is not int:
        raise ValueError("Indices must be integers.")

    if not (0 <= i < len(tour) and 0 <= j < len(tour)):
        raise ValueError("Swap indices are out of range.")

    result = list(tour)
    result[i], result[j] = result[j], result[i]

    return result


def insertion(tour: Sequence[int], i: int, j: int) -> list[int]:
    """
    Remove the element at position i and insert it at position j.

    Return a new list without modifying the original tour.
    """
    if type(i) is not int or type(j) is not int:
        raise ValueError("Indices must be integers.")

    if not (0 <= i < len(tour) and 0 <= j < len(tour)):
        raise ValueError("Insertion indices are out of range.")

    result = list(tour)

    city = result.pop(i)
    result.insert(j, city)

    return result


def two_opt(tour: Sequence[int], i: int, j: int) -> list[int]:
    """Reverse the inclusive segment [i, j]; indices must satisfy i < j."""
    if type(i) is not int or type(j) is not int:
        raise ValueError("Indices must be integers.")

    if not (0 <= i < j < len(tour)):
        raise ValueError("Require 0 <= i < j < len(tour).")

    result = list(tour)
    result[i:j + 1] = reversed(result[i:j + 1])

    return result
def three_opt(tour: Sequence[int]) -> list[int]:
    """TODO: implement a documented 3-opt neighborhood move.

    The exact reconnection strategy should be chosen and tested against the
    reference paper; a random permutation is not a substitute for 3-opt.
    """
    raise NotImplementedError(
        "Implement 3-opt after reviewing the full DBA paper."
    )