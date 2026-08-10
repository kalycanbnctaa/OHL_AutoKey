import math

import pytest

from app.models.dictionary_entry import DictionaryEntry
from app.utils.scoring import calculate_total_frequency, calculate_word_cost


def test_calculate_total_frequency() -> None:
    entries = [
        DictionaryEntry(word="a", frequency=10),
        DictionaryEntry(word="b", frequency=20),
        DictionaryEntry(word="c", frequency=30),
    ]

    assert calculate_total_frequency(entries) == 60


def test_calculate_total_frequency_empty() -> None:
    assert calculate_total_frequency([]) == 0


def test_calculate_word_cost() -> None:
    total_frequency = 1000

    cost = calculate_word_cost(frequency=100, total_frequency=total_frequency)

    assert cost == pytest.approx(math.log(1000 / 100))


def test_calculate_word_cost_clamps_frequency_to_minimum_one() -> None:
    total_frequency = 1000

    cost_zero = calculate_word_cost(frequency=0, total_frequency=total_frequency)
    cost_one = calculate_word_cost(frequency=1, total_frequency=total_frequency)

    assert cost_zero == cost_one == pytest.approx(math.log(1000))


def test_calculate_word_cost_rejects_non_positive_total_frequency() -> None:
    with pytest.raises(ValueError):
        calculate_word_cost(frequency=10, total_frequency=0)

    with pytest.raises(ValueError):
        calculate_word_cost(frequency=10, total_frequency=-5)


def test_calculate_word_cost_rejects_negative_frequency() -> None:
    with pytest.raises(ValueError):
        calculate_word_cost(frequency=-1, total_frequency=1000)


def test_calculate_word_cost_rejects_invalid_types() -> None:
    with pytest.raises(TypeError):
        calculate_word_cost(frequency=1.5, total_frequency=1000)

    with pytest.raises(TypeError):
        calculate_word_cost(frequency=10, total_frequency=1.5)