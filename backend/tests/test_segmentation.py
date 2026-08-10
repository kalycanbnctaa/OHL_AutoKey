import json
from pathlib import Path

import pytest

from app.core.segmentation import segment_text
from app.services.dictionary_service import DictionaryService


@pytest.fixture
def dictionary_service(tmp_path: Path):
    path = tmp_path / "kamus.json"
    path.write_text(
        json.dumps({
            "program": 1000,
            "dinamis": 500,
            "programdinamis": 1,
            "ini": 2000,
            "cukup": 300,
            "sulit": 150,
            "a": 10,
            "b": 20,
            "ab": 5,
            "c": 30,
        }),
        encoding="utf-8"
    )
    service = DictionaryService(path)
    service.load()
    return service


def test_segment_text_success(dictionary_service):
    word_freq = {word: entry.frequency for word, entry in dictionary_service.entries.items()}
    total_freq = dictionary_service.total_frequency

    result = segment_text("programdinamis", word_freq, total_freq)
    assert result is not None
    assert result.words == ["program", "dinamis"]
    assert result.result == "program dinamis"
    assert len(result.dp) == len("programdinamis") + 1
    assert result.dp[0] == 0.0
    assert result.cost > 0


def test_segment_text_with_multiple_words(dictionary_service):
    word_freq = {word: entry.frequency for word, entry in dictionary_service.entries.items()}
    total_freq = dictionary_service.total_frequency

    result = segment_text("inicukupsulit", word_freq, total_freq)
    assert result is not None
    assert result.words == ["ini", "cukup", "sulit"]
    assert result.result == "ini cukup sulit"


def test_segment_text_empty(dictionary_service):
    word_freq = {word: entry.frequency for word, entry in dictionary_service.entries.items()}
    total_freq = dictionary_service.total_frequency

    result = segment_text("", word_freq, total_freq)
    assert result is None


def test_segment_text_no_valid_segmentation(dictionary_service):
    word_freq = {word: entry.frequency for word, entry in dictionary_service.entries.items()}
    total_freq = dictionary_service.total_frequency

    result = segment_text("xyz", word_freq, total_freq)
    assert result is None


def test_segment_text_prefers_lower_cost(dictionary_service):
    word_freq = {word: entry.frequency for word, entry in dictionary_service.entries.items()}
    total_freq = dictionary_service.total_frequency

    result = segment_text("programdinamis", word_freq, total_freq)
    assert result is not None
    assert result.words == ["program", "dinamis"]


def test_segment_text_single_word(dictionary_service):
    word_freq = {word: entry.frequency for word, entry in dictionary_service.entries.items()}
    total_freq = dictionary_service.total_frequency

    result = segment_text("program", word_freq, total_freq)
    assert result is not None
    assert result.words == ["program"]
    assert result.result == "program"


def test_segment_text_multiple_optimal_segmentations(dictionary_service):
    word_freq = {word: entry.frequency for word, entry in dictionary_service.entries.items()}
    total_freq = dictionary_service.total_frequency

    result = segment_text("ab", word_freq, total_freq)
    assert result is not None
    assert result.result in ["ab", "a b"]


def test_segment_text_cost_calculation(dictionary_service):
    word_freq = {word: entry.frequency for word, entry in dictionary_service.entries.items()}
    total_freq = dictionary_service.total_frequency

    result = segment_text("program", word_freq, total_freq)
    assert result is not None
    import math
    expected_cost = math.log(total_freq / 1000)  
    assert result.cost == pytest.approx(expected_cost, rel=1e-9)


def test_segment_text_choice_traceback(dictionary_service):
    word_freq = {word: entry.frequency for word, entry in dictionary_service.entries.items()}
    total_freq = dictionary_service.total_frequency

    result = segment_text("programdinamis", word_freq, total_freq)
    assert result is not None
    assert result.choices is not None
    words = []
    i = len("programdinamis")
    while i > 0:
        j = result.choices[i]
        assert j >= 0
        words.append("programdinamis"[j:i])
        i = j
    words.reverse()
    assert words == result.words