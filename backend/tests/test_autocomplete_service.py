import pytest

from app.services.autocomplete_service import AutocompleteService
from app.services.dictionary_service import DictionaryService


@pytest.fixture
def service(tmp_path):
    import json

    path = tmp_path / "kamus.json"
    path.write_text(
        json.dumps(
            {
                "program": 1000,
                "programming": 800,
                "programa": 50,
                "progresif": 300,
                "progres": 400,
            }
        ),
        encoding="utf-8",
    )

    dictionary_service = DictionaryService(path)
    dictionary_service.load()

    return AutocompleteService(dictionary_service)


def test_get_suggestions_ranked_by_frequency(service) -> None:
    suggestions = service.get_suggestions("prog")

    words = [entry.word for entry in suggestions]

    assert words == [
        "program",
        "programming",
        "progres",
        "progresif",
        "programa",
    ]


def test_get_suggestions_respects_top_n(service) -> None:
    suggestions = service.get_suggestions("prog", top_n=2)

    assert len(suggestions) == 2


def test_get_suggestions_empty_prefix_returns_empty(service) -> None:
    assert service.get_suggestions("") == []
    assert service.get_suggestions("   ") == []


def test_get_suggestions_unknown_prefix_returns_empty(service) -> None:
    assert service.get_suggestions("xyz") == []


def test_get_suggestions_top_n_is_bounded(service) -> None:
    suggestions = service.get_suggestions("prog", top_n=1000)

    assert len(suggestions) <= 20


def test_get_suggestions_rejects_invalid_prefix_type(service) -> None:
    with pytest.raises(TypeError):
        service.get_suggestions(123)