import pytest

from app.core.levenshtein import compute_distance_table, levenshtein_distance

def test_distance_between_kitten_and_sitting() -> None:
    assert levenshtein_distance("kitten", "sitting") == 3

def test_distance_table_basis_and_recurrence() -> None:
    result = compute_distance_table("kitten", "sitting")
    assert result.distance == 3
    assert result.table[0] == [0, 1, 2, 3, 4, 5, 6, 7]
    assert [row[0] for row in result.table] == [0, 1, 2, 3, 4, 5, 6]
    assert result.table[-1][-1] == 3

def test_distance_same_word_is_zero() -> None:
    assert levenshtein_distance("kata", "kata") == 0
    result = compute_distance_table("kata", "kata")
    assert result.distance == 0

def test_distance_empty_strings() -> None:
    assert levenshtein_distance("", "") == 0
    assert levenshtein_distance("kata", "") == 4
    assert levenshtein_distance("", "kata") == 4

def test_distance_is_symmetric() -> None:
    assert levenshtein_distance("kucing", "kuceng") == levenshtein_distance(
        "kuceng", "kucing"
    )

def test_distance_single_substitution() -> None:
    assert levenshtein_distance("kata", "mata") == 1

def test_distance_single_insertion() -> None:
    assert levenshtein_distance("kata", "katak") == 1

def test_distance_single_deletion() -> None:
    assert levenshtein_distance("katak", "kata") == 1

def test_distance_greater_than_two() -> None:
    assert levenshtein_distance("kalimt", "monyet") > 2

def test_distance_exactly_two() -> None:
    assert levenshtein_distance("kucing", "kuceng") == 1
    assert levenshtein_distance("kucing", "kucang") == 1

def test_distance_exactly_three() -> None:
    assert levenshtein_distance("kitten", "sitting") == 3

def test_distance_completely_different() -> None:
    assert levenshtein_distance("abcdefghij", "klmnopqrst") > 5

def test_invalid_input_type_is_rejected() -> None:
    with pytest.raises(TypeError):
        levenshtein_distance(123, "kata")
    with pytest.raises(TypeError):
        levenshtein_distance("kata", None)

def test_compute_distance_table_invalid_type_is_rejected() -> None:
    with pytest.raises(TypeError):
        compute_distance_table(123, "kata")

def test_distance_with_unicode() -> None:
    assert levenshtein_distance("café", "cafe") == 1
    assert levenshtein_distance("anak-anak", "anak") == 5

def test_distance_table_dimensions() -> None:
    result = compute_distance_table("kata", "kata")
    assert len(result.table) == 5
    assert len(result.table[0]) == 5

def test_distance_table_last_row_is_distance() -> None:
    result = compute_distance_table("kucing", "kuceng")
    assert result.table[-1][-1] == result.distance

def test_distance_table_basis_row_zero() -> None:
    result = compute_distance_table("abc", "xyz")
    assert result.table[0] == [0, 1, 2, 3]
    for i in range(len("abc") + 1):
        assert result.table[i][0] == i