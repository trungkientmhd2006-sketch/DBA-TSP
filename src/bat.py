"""Bat representation and parameters for the discrete algorithm."""

from dataclasses import dataclass


@dataclass
class Bat:
    tour: list[int]
    cost: float
    loudness: float = 1.0
    pulse_rate: float = 0.5
