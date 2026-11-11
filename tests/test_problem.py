
import pytest

from src.problem import (
    is_valid_tour,
    tour_length,
    read_tsplib,
    calculate_distance_matrix,
)


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


def test_read_tsplib():
    cities = read_tsplib("data/instances/eil51.tsp")

    assert len(cities) == 51
    assert cities[0] == (37.0, 52.0)
    assert cities[-1] == (30.0, 40.0)


def test_distance_matrix_size():
    coordinates = [(0, 0), (3, 4), (6, 0)]
    distances = calculate_distance_matrix(coordinates)

    assert len(distances) == 3
    assert all(len(row) == 3 for row in distances)


def test_distance_matrix_symmetry():
    coordinates = [(0, 0), (3, 4), (6, 0)]
    distances = calculate_distance_matrix(coordinates)

    for i in range(3):
        for j in range(3):
            assert distances[i][j] == distances[j][i]


def test_distance_matrix_diagonal():
    coordinates = [(0, 0), (3, 4), (6, 0)]
    distances = calculate_distance_matrix(coordinates)

    for i in range(3):
        assert distances[i][i] == 0


def test_euc_2d_rounding():
    distances = calculate_distance_matrix([(0, 0), (3, 4)])

    assert distances[0][1] == 5
    assert distances[1][0] == 5


def test_read_tsplib_rejects_duplicate_ids(tmp_path):
    file = tmp_path / "duplicate.tsp"
    file.write_text(
        "NAME: test\n"
        "TYPE: TSP\n"
        "DIMENSION: 2\n"
        "EDGE_WEIGHT_TYPE: EUC_2D\n"
        "NODE_COORD_SECTION\n"
        "1 0 0\n"
        "1 3 4\n"
        "EOF\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate"):
        read_tsplib(file)


def test_read_tsplib_rejects_missing_city(tmp_path):
    file = tmp_path / "missing.tsp"
    file.write_text(
        "NAME: test\n"
        "TYPE: TSP\n"
        "DIMENSION: 3\n"
        "EDGE_WEIGHT_TYPE: EUC_2D\n"
        "NODE_COORD_SECTION\n"
        "1 0 0\n"
        "2 3 4\n"
        "4 5 6\n"
        "EOF\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        read_tsplib(file)


def test_distance_matrix_rejects_invalid_coordinates():
    with pytest.raises(ValueError):
        calculate_distance_matrix([(0, 0), (float("inf"), 4)])


def test_tour_length_rejects_invalid_tour():
    distances = [
        [0, 2, 9],
        [2, 0, 3],
        [9, 3, 0],
    ]

    with pytest.raises(ValueError):
        tour_length([0, 0, 2], distances)


def test_tour_length_rejects_non_square_matrix():
    distances = [
        [0, 2],
        [2, 0, 3],
    ]

    with pytest.raises(ValueError):
        tour_length([0, 1], distances)
