import math
from collections.abc import Iterable

from app.models.dictionary_entry import DictionaryEntry

MIN_EFFECTIVE_FREQUENCY = 1


def calculate_total_frequency(entries: Iterable[DictionaryEntry]) -> int:
    return sum(entry.frequency for entry in entries)


def calculate_word_cost(frequency: int, total_frequency: int) -> float:
    if isinstance(frequency, bool) or not isinstance(frequency, int):
        raise TypeError("frequency must be an integer")

    if isinstance(total_frequency, bool) or not isinstance(total_frequency, int):
        raise TypeError("total_frequency must be an integer")

    if frequency < 0:
        raise ValueError("frequency must not be negative")

    if total_frequency <= 0:
        raise ValueError("total_frequency must be positive")

    effective_frequency = max(frequency, MIN_EFFECTIVE_FREQUENCY)

    return math.log(total_frequency / effective_frequency)