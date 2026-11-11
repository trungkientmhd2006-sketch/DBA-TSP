
import pytest

from src.operators import hamming_distance, swap, insertion, two_opt


def test_hamming_distance():
    assert hamming_distance([0, 1, 2], [0, 2, 1]) == 2


def test_two_opt_preserves_permutation():
    assert two_opt([0, 1, 2, 3, 4], 1, 3) == [0, 3, 2, 1, 4]


# SWAP TESTS

def test_swap_two_positions():
    assert swap([0, 1, 2, 3, 4], 1, 3) == [0, 3, 2, 1, 4]


def test_swap_preserves_original_tour():
    tour = [0, 1, 2, 3, 4]
    result = swap(tour, 1, 3)

    assert tour == [0, 1, 2, 3, 4]
    assert result != tour


def test_swap_same_position():
    tour = [0, 1, 2, 3]
    result = swap(tour, 2, 2)

    assert result == tour
    assert result is not tour


def test_swap_preserves_permutation():
    tour = [0, 1, 2, 3, 4]
    result = swap(tour, 1, 4)

    assert sorted(result) == sorted(tour)


def test_swap_rejects_negative_index():
    with pytest.raises(ValueError):
        swap([0, 1, 2], -1, 2)


def test_swap_rejects_out_of_range_index():
    with pytest.raises(ValueError):
        swap([0, 1, 2], 0, 3)


def test_swap_rejects_non_integer_index():
    with pytest.raises(ValueError):
        swap([0, 1, 2], 0, 1.5)


# INSERTION TESTS

def test_insertion_moves_city():
    tour = [0, 1, 2, 3, 4]

    result = insertion(tour, 1, 3)

    assert result == [0, 2, 3, 1, 4]


def test_insertion_preserves_original_tour():
    tour = [0, 1, 2, 3, 4]

    result = insertion(tour, 1, 3)

    assert tour == [0, 1, 2, 3, 4]
    assert result != tour


def test_insertion_same_position():
    tour = [0, 1, 2, 3]

    result = insertion(tour, 2, 2)

    assert result == tour
    assert result is not tour


def test_insertion_preserves_permutation():
    tour = [0, 1, 2, 3, 4]

    result = insertion(tour, 1, 4)

    assert sorted(result) == sorted(tour)


def test_insertion_rejects_negative_index():
    with pytest.raises(ValueError):
        insertion([0, 1, 2], -1, 2)


def test_insertion_rejects_out_of_range_index():
    with pytest.raises(ValueError):
        insertion([0, 1, 2], 0, 3)


def test_insertion_rejects_non_integer_index():
    with pytest.raises(ValueError):
        insertion([0, 1, 2], 0, 1.5)





# INVERSION / TWO-OPT TESTS

def test_two_opt_preserves_original_tour():
    tour = [0, 1, 2, 3, 4]

    result = two_opt(tour, 1, 3)

    assert tour == [0, 1, 2, 3, 4]
    assert result != tour


def test_two_opt_preserves_permutation():
    tour = [0, 1, 2, 3, 4]

    result = two_opt(tour, 1, 3)

    assert sorted(result) == sorted(tour)


def test_two_opt_reverses_two_elements():
    tour = [0, 1, 2, 3]

    result = two_opt(tour, 1, 2)

    assert result == [0, 2, 1, 3]


def test_two_opt_rejects_same_index():
    with pytest.raises(ValueError):
        two_opt([0, 1, 2], 1, 1)


def test_two_opt_rejects_negative_index():
    with pytest.raises(ValueError):
        two_opt([0, 1, 2], -1, 2)


def test_two_opt_rejects_out_of_range_index():
    with pytest.raises(ValueError):
        two_opt([0, 1, 2], 0, 3)
