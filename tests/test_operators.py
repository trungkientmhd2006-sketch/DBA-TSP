from src.operators import hamming_distance, two_opt


def test_hamming_distance():
    assert hamming_distance([0, 1, 2], [0, 2, 1]) == 2


def test_two_opt_preserves_permutation():
    assert two_opt([0, 1, 2, 3, 4], 1, 3) == [0, 3, 2, 1, 4]
