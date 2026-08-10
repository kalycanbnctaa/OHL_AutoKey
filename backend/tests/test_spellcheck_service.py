import json
from pathlib import Path

import pytest

from app.services.dictionary_service import DictionaryService
from app.services.spellcheck_service import SpellCheckService, tokenize


@pytest.fixture
def service(tmp_path: Path) -> SpellCheckService:
    path = tmp_path / "kamus.json"
    path.write_text(
        json.dumps(
            {
                "kalimat": 2295,
                "kali": 28857,
                "kulit": 5715,
                "kelima": 3242,
                "salim": 757,
                "kalimantan": 500,
                "monyet": 900,
            }
        ),
        encoding="utf-8",
    )

    dictionary_service = DictionaryService(path)
    dictionary_service.load()

    return SpellCheckService(dictionary_service)


def test_find_words_within_distance_includes_distance_within_bound(
    service: SpellCheckService,
) -> None:
    candidates = service.find_words_within_distance("kalimt", max_distance=2)
    words = [candidate.word for candidate in candidates]

    assert "kalimat" in words


def test_find_words_within_distance_excludes_distance_greater_than_max(
    service: SpellCheckService,
) -> None:
    candidates = service.find_words_within_distance("kalimt", max_distance=2)
    words = [candidate.word for candidate in candidates]

    assert "kalimantan" not in words
    assert "monyet" not in words


def test_find_words_within_distance_ranking(
    service: SpellCheckService,
) -> None:
    candidates = service.find_words_within_distance("kalimt", max_distance=2)

    distances = [candidate.distance for candidate in candidates]
    assert distances == sorted(distances)

    for i in range(len(candidates) - 1):
        if candidates[i].distance == candidates[i + 1].distance:
            assert candidates[i].frequency >= candidates[i + 1].frequency


def test_find_words_within_distance_same_word_returns_distance_zero(
    service: SpellCheckService,
) -> None:
    candidates = service.find_words_within_distance("kalimat", max_distance=2)

    assert candidates[0].word == "kalimat"
    assert candidates[0].distance == 0


def test_find_words_within_distance_empty_input_returns_empty(
    service: SpellCheckService,
) -> None:
    assert service.find_words_within_distance("", max_distance=2) == []
    assert service.find_words_within_distance("   ", max_distance=2) == []


def test_find_words_within_distance_rejects_invalid_max_distance(
    service: SpellCheckService,
) -> None:
    with pytest.raises(ValueError):
        service.find_words_within_distance("kata", max_distance=-1)

    with pytest.raises(TypeError):
        service.find_words_within_distance("kata", max_distance=1.5)

    with pytest.raises(ValueError):
        service.find_words_within_distance("kata", max_distance=10)


def test_find_words_within_distance_respects_limit(
    service: SpellCheckService,
) -> None:
    candidates = service.find_words_within_distance(
        "kalimt", max_distance=2, limit=2
    )

    assert len(candidates) <= 2


def test_is_valid_word(service: SpellCheckService) -> None:
    assert service.is_valid_word("kalimat")
    assert service.is_valid_word("KALIMAT")
    assert not service.is_valid_word("kalimt")
    assert not service.is_valid_word("")


def test_is_valid_word_rejects_invalid_type(
    service: SpellCheckService,
) -> None:
    with pytest.raises(TypeError):
        service.is_valid_word(123)


def test_tokenize_returns_words_with_offsets() -> None:
    tokens = tokenize("saya suka kalimt")

    assert tokens == [
        ("saya", 0, 4),
        ("suka", 5, 9),
        ("kalimt", 10, 16),
    ]


def test_check_text_flags_unknown_words(service: SpellCheckService) -> None:
    issues = service.check_text("kalimat kali kalimt")
    flagged_words = [issue.word for issue in issues]
    assert "kalimt" in flagged_words
    assert "kalimat" not in flagged_words
    assert "kali" not in flagged_words


def test_check_text_empty_string_returns_no_issues(
    service: SpellCheckService,
) -> None:
    assert service.check_text("") == []


def test_check_text_rejects_invalid_type(service: SpellCheckService) -> None:
    with pytest.raises(TypeError):
        service.check_text(123)