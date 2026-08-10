import json
from pathlib import Path

import pytest

from app.services.dictionary_service import DictionaryService


def create_dictionary_file(
    tmp_path: Path,
    data: dict,
) -> Path:
    path = tmp_path / "kamus.json"
    path.write_text(
        json.dumps(data, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def test_load_dictionary(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "Rumah": 100,
            "Makan": 80,
            "  Minum  ": 60,
            "": 999,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    assert service.is_loaded
    assert service.word_count == 3
    assert service.entries["rumah"].frequency == 100
    assert service.entries["makan"].frequency == 80
    assert service.entries["minum"].frequency == 60
    assert service.total_frequency == 240

    assert service.trie.search("rumah")
    assert service.trie.search("MAKAN")
    assert service.trie.search("minum")


def test_load_is_idempotent(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": 10,
            "api": 20,
        },
    )

    service = DictionaryService(dictionary_path)

    service.load()

    first_word_count = service.word_count
    first_node_count = service.node_count
    first_total_frequency = service.total_frequency
    first_entries = dict(service.entries)

    service.load()

    assert service.is_loaded
    assert service.word_count == first_word_count
    assert service.node_count == first_node_count
    assert service.total_frequency == first_total_frequency
    assert service.entries == first_entries


def test_reload_replaces_previous_dictionary(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": 10,
            "api": 20,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    dictionary_path.write_text(
        json.dumps(
            {
                "komputer": 100,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    service.load()

    assert service.word_count == 1
    assert service.search("apel") is None
    assert service.search("komputer") is not None
    assert service.total_frequency == 100


def test_search_returns_dictionary_entry(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "Komputer": 42,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    entry = service.search("KOMPUTER")

    assert entry is not None
    assert entry.word == "komputer"
    assert entry.frequency == 42


def test_search_normalizes_word(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "komputer": 42,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    assert service.search("  KOMPUTER  ") is not None


def test_search_unknown_word_returns_none(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "komputer": 42,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    assert service.search("internet") is None
    assert service.search("") is None
    assert service.search("   ") is None


def test_search_invalid_word_type_is_rejected(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "komputer": 42,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    with pytest.raises(TypeError):
        service.search(123)


def test_starts_with(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "komputer": 42,
            "komputasi": 30,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    assert service.starts_with("kom")
    assert service.starts_with("KOM")
    assert service.starts_with("")
    assert not service.starts_with("xyz")


def test_get_suggestions(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": 10,
            "aplikasi": 50,
            "api": 30,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    suggestions = service.get_suggestions("ap", 2)

    assert [(entry.word, entry.frequency) for entry in suggestions] == [
        ("aplikasi", 50),
        ("api", 30),
    ]


def test_get_suggestions_with_empty_prefix(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": 10,
            "aplikasi": 50,
            "komputer": 100,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    suggestions = service.get_suggestions("")

    assert [(entry.word, entry.frequency) for entry in suggestions] == [
        ("komputer", 100),
        ("aplikasi", 50),
        ("apel", 10),
    ]


def test_get_suggestions_unknown_prefix_returns_empty(
    tmp_path: Path,
) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": 10,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    assert service.get_suggestions("xyz") == []


def test_get_suggestions_respects_top_n(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": 10,
            "aplikasi": 50,
            "api": 30,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    suggestions = service.get_suggestions("ap", 2)

    assert len(suggestions) == 2


def test_get_suggestions_rejects_invalid_top_n(
    tmp_path: Path,
) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": 10,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    with pytest.raises(TypeError):
        service.get_suggestions("ap", True)

    with pytest.raises(TypeError):
        service.get_suggestions("ap", 1.5)

    with pytest.raises(ValueError):
        service.get_suggestions("ap", -1)


def test_missing_dictionary_file_raises_error(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.json"

    service = DictionaryService(missing_path)

    with pytest.raises(FileNotFoundError):
        service.load()

    assert not service.is_loaded


def test_dictionary_path_must_be_file(tmp_path: Path) -> None:
    dictionary_path = tmp_path / "kamus.json"
    dictionary_path.mkdir()

    service = DictionaryService(dictionary_path)

    with pytest.raises(ValueError, match="not a file"):
        service.load()

    assert not service.is_loaded


def test_invalid_json_raises_error(tmp_path: Path) -> None:
    path = tmp_path / "kamus.json"
    path.write_text(
        '{"apel": 10,',
        encoding="utf-8",
    )

    service = DictionaryService(path)

    with pytest.raises(ValueError, match="invalid JSON"):
        service.load()

    assert not service.is_loaded


def test_dictionary_must_be_json_object(tmp_path: Path) -> None:
    path = tmp_path / "kamus.json"
    path.write_text(
        json.dumps(["apel", "api"]),
        encoding="utf-8",
    )

    service = DictionaryService(path)

    with pytest.raises(ValueError, match="JSON object"):
        service.load()

    assert not service.is_loaded


def test_invalid_word_type_raises_error(tmp_path: Path) -> None:
    path = tmp_path / "kamus.json"
    path.write_text(
        '{"apel": 10}',
        encoding="utf-8",
    )

    service = DictionaryService(path)
    service.load()

    assert service.search("apel") is not None


def test_invalid_frequency_raises_error(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": "invalid",
        },
    )

    service = DictionaryService(dictionary_path)

    with pytest.raises(ValueError, match="Invalid frequency"):
        service.load()


def test_float_frequency_raises_error(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": 1.5,
        },
    )

    service = DictionaryService(dictionary_path)

    with pytest.raises(ValueError, match="Invalid frequency"):
        service.load()


def test_boolean_frequency_raises_error(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": True,
        },
    )

    service = DictionaryService(dictionary_path)

    with pytest.raises(ValueError, match="Invalid frequency"):
        service.load()


def test_negative_frequency_raises_error(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "apel": -10,
        },
    )

    service = DictionaryService(dictionary_path)

    with pytest.raises(ValueError, match="must not be negative"):
        service.load()


def test_duplicate_normalized_word_raises_error(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "Rumah": 100,
            " rumah ": 50,
        },
    )

    service = DictionaryService(dictionary_path)

    with pytest.raises(ValueError, match="Duplicate dictionary word"):
        service.load()


def test_empty_normalized_words_are_ignored(tmp_path: Path) -> None:
    dictionary_path = create_dictionary_file(
        tmp_path,
        {
            "": 100,
            "   ": 200,
            "apel": 50,
        },
    )

    service = DictionaryService(dictionary_path)
    service.load()

    assert service.word_count == 1
    assert service.total_frequency == 50
    assert list(service.entries) == ["apel"]