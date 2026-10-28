import pytest

from src.problem import is_valid_tour, tour_length


def test_closed_tour_length():
    distances = [
        [0, 2, 9],
        [2, 0, 3],
        [9, 3, 0],
    ]
    assert tour_length([0, 1, 2], distances) == 14


def test_valid_tour():
    assert is_valid_tour([2, 0, 1], 3)
    assert not is_valid_tour([0, 0, 1], 3)
    assert not is_valid_tour([0, 1], 3)


def test_length_rejects_too_short_tour():
    with pytest.raises(ValueError):
        tour_length([0], [[0]])
