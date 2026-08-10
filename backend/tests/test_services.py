import json
from pathlib import Path

import pytest

from app.services.autocomplete_service import AutocompleteService
from app.services.dictionary_service import DictionaryService
from app.services.spellcheck_service import SpellCheckService
from app.services.segmentation_service import SegmentationService
from app.services.smart_trim_service import SmartTrimService
from app.services.bigram_service import BigramService


@pytest.fixture
def dictionary_service(tmp_path: Path):
    path = tmp_path / "kamus.json"
    path.write_text(
        json.dumps({
            "program": 1000,
            "programming": 800,
            "progres": 400,
            "progresif": 300,
            "programa": 50,
            "kalimat": 2295,
            "kali": 28857,
            "kulit": 5715,
            "kelima": 3242,
            "salim": 757,
            "kalimantan": 500,
            "monyet": 900,
            "dinamis": 500,
            "ini": 2000,
            "cukup": 300,
            "sulit": 150,
            "a": 10,
            "b": 20,
            "ab": 5,
        }),
        encoding="utf-8"
    )
    service = DictionaryService(path)
    service.load()
    return service


def test_autocomplete_service_get_suggestions(dictionary_service):
    service = AutocompleteService(dictionary_service)
    suggestions = service.get_suggestions("prog")
    words = [entry.word for entry in suggestions]
    assert words == ["program", "programming", "progres", "progresif", "programa"]


def test_autocomplete_service_empty_prefix(dictionary_service):
    service = AutocompleteService(dictionary_service)
    assert service.get_suggestions("") == []
    assert service.get_suggestions("   ") == []


def test_autocomplete_service_unknown_prefix(dictionary_service):
    service = AutocompleteService(dictionary_service)
    assert service.get_suggestions("xyz") == []


def test_autocomplete_service_top_n_bounded(dictionary_service):
    service = AutocompleteService(dictionary_service)
    suggestions = service.get_suggestions("prog", top_n=1000)
    assert len(suggestions) <= 20


def test_autocomplete_service_rejects_invalid_prefix_type(dictionary_service):
    service = AutocompleteService(dictionary_service)
    with pytest.raises(TypeError):
        service.get_suggestions(123)


def test_spellcheck_service_is_valid_word(dictionary_service):
    service = SpellCheckService(dictionary_service)
    assert service.is_valid_word("kalimat") is True
    assert service.is_valid_word("KALIMAT") is True
    assert service.is_valid_word("kalimt") is False
    assert service.is_valid_word("") is False


def test_spellcheck_service_find_words_within_distance(dictionary_service):
    service = SpellCheckService(dictionary_service)
    candidates = service.find_words_within_distance("kalimt", max_distance=2)
    words = [c.word for c in candidates]
    assert "kalimat" in words
    assert "kali" in words 
    assert "kalimantan" not in words  


def test_spellcheck_service_find_words_ranking(dictionary_service):
    service = SpellCheckService(dictionary_service)
    candidates = service.find_words_within_distance("kalimt", max_distance=2)
    distances = [c.distance for c in candidates]
    assert distances == sorted(distances)
    for i in range(len(candidates) - 1):
        if candidates[i].distance == candidates[i + 1].distance:
            assert candidates[i].frequency >= candidates[i + 1].frequency


def test_spellcheck_service_check_text(dictionary_service):
    service = SpellCheckService(dictionary_service)
    issues = service.check_text("kalimat kali kalimt")
    flagged_words = [issue.word for issue in issues]
    assert "kalimt" in flagged_words
    assert "kalimat" not in flagged_words
    assert "kali" not in flagged_words


def test_segmentation_service_segment(dictionary_service):
    service = SegmentationService(dictionary_service)
    result = service.segment("programdinamis")
    assert result is not None
    assert result.words == ["program", "dinamis"]
    assert result.result == "program dinamis"


def test_segmentation_service_empty_text(dictionary_service):
    service = SegmentationService(dictionary_service)
    result = service.segment("")
    assert result is None


def test_segmentation_service_no_valid_segmentation(dictionary_service):
    service = SegmentationService(dictionary_service)
    result = service.segment("xyz")
    assert result is None


def test_smart_trim_service_trim(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("program dinamis ini cukup sulit", 15)
    assert result is not None
    assert result.total_weight <= 15
    assert len(result.items) > 0


def test_smart_trim_service_empty_text(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("", 10)
    assert result is None


def test_smart_trim_service_no_valid_words(dictionary_service):
    service = SmartTrimService(dictionary_service)
    result = service.trim("xyz abc", 10)
    assert result is None


def test_bigram_service_basic(dictionary_service):
    service = BigramService()
    session_id = "test"
    service.record_pair(session_id, "data", "science")
    service.record_pair(session_id, "data", "science")
    service.record_pair(session_id, "data", "analysis")
    stats = service.get_statistics(session_id)
    assert stats["total_pairs"] == 3
    assert stats["unique_pairs"] == 2

    candidates = [("science", 100), ("analysis", 200), ("program", 50)]
    scored = service.rerank_suggestions(session_id, "data", candidates)
    assert scored[0][0] in ("science", "analysis")
    assert scored[-1][0] == "program"