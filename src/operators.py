"""Discrete permutation operators for DBA/IBA."""

from collections.abc import Sequence


def hamming_distance(a: Sequence[int], b: Sequence[int]) -> int:
    """Count positions at which two same-length tours differ."""
    if len(a) != len(b):
        raise ValueError("Tours must have the same length.")
    return sum(x != y for x, y in zip(a, b))


def two_opt(tour: Sequence[int], i: int, j: int) -> list[int]:
    """Reverse the inclusive segment [i, j]; indices must satisfy i < j."""
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
    raise NotImplementedError("Implement 3-opt after reviewing the full DBA paper.")
