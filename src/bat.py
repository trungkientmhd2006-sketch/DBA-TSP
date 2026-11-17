
"""Bat representation and parameters for the discrete bat algorithm."""

from dataclasses import dataclass


@dataclass
class Bat:
    """Represent one bat and its TSP solution."""

    tour: list[int]
    cost: float

    # Number of 2-opt moves
    velocity: int = 1

    # Echolocation parameters
    loudness: float = 0.8
    pulse_rate: float = 0.2

    # Initial pulse rate, used in the update equation
    initial_pulse_rate: float = 0.2
