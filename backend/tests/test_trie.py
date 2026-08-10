import pytest

from app.core.trie import Trie


def test_insert_and_search() -> None:
    trie = Trie()
    trie.insert("komputer", 100)
    assert trie.search("komputer") is True
    assert trie.search("KOMPUTER") is True
    assert trie.search("komputasi") is False
    assert trie.word_count == 1


def test_insert_same_word_updates_frequency() -> None:
    trie = Trie()
    trie.insert("python", 10)
    trie.insert("python", 25)
    assert trie.word_count == 1
    assert trie.search("python") is True
    assert trie.get_suggestions("python") == [("python", 25)]


def test_insert_normalizes_word() -> None:
    trie = Trie()
    trie.insert("  Komputer  ", 100)
    assert trie.search("komputer") is True
    assert trie.search(" KOMPUTER ") is True
    assert trie.word_count == 1


def test_insert_creates_expected_nodes() -> None:
    trie = Trie()
    trie.insert("cat", 1)
    assert trie.node_count == 4
    assert trie.word_count == 1


def test_insert_zero_frequency() -> None:
    trie = Trie()
    trie.insert("apel", 0)
    assert trie.search("apel") is True
    assert trie.get_suggestions("ap") == [("apel", 0)]


def test_starts_with() -> None:
    trie = Trie()
    trie.insert("komputer", 100)
    trie.insert("komputasi", 80)
    assert trie.starts_with("kom") is True
    assert trie.starts_with("KOM") is True
    assert trie.starts_with("komp") is True
    assert trie.starts_with("") is True
    assert trie.starts_with("   ") is True
    assert trie.starts_with("xyz") is False


def test_starts_with_word_bukan_prefix() -> None:
    trie = Trie()
    trie.insert("program", 100)
    assert trie.starts_with("prog") is True
    assert trie.starts_with("program") is True
    assert trie.starts_with("programming") is False
    assert trie.starts_with("pr") is True


def test_get_suggestions_orders_by_frequency_then_word() -> None:
    trie = Trie()
    trie.insert("apel", 10)
    trie.insert("aplikasi", 50)
    trie.insert("api", 30)
    trie.insert("aplikatif", 50)
    assert trie.get_suggestions("ap") == [
        ("aplikasi", 50),
        ("aplikatif", 50),
        ("api", 30),
        ("apel", 10),
    ]


def test_get_suggestions_normalizes_prefix() -> None:
    trie = Trie()
    trie.insert("aplikasi", 50)
    trie.insert("api", 30)
    assert trie.get_suggestions(" AP ") == [
        ("aplikasi", 50),
        ("api", 30),
    ]


def test_get_suggestions_empty_prefix_returns_global_top() -> None:
    trie = Trie()
    trie.insert("apel", 10)
    trie.insert("aplikasi", 50)
    trie.insert("komputer", 100)
    assert trie.get_suggestions("") == [
        ("komputer", 100),
        ("aplikasi", 50),
        ("apel", 10),
    ]


def test_get_suggestions_respects_top_n() -> None:
    trie = Trie()
    trie.insert("apel", 10)
    trie.insert("aplikasi", 50)
    trie.insert("api", 30)
    assert trie.get_suggestions("ap", 2) == [
        ("aplikasi", 50),
        ("api", 30),
    ]


def test_get_suggestions_top_n_larger_than_results() -> None:
    trie = Trie()
    trie.insert("apel", 10)
    assert trie.get_suggestions("ap", 100) == [("apel", 10)]


def test_get_suggestions_unknown_prefix_returns_empty() -> None:
    trie = Trie()
    trie.insert("apel", 10)
    assert trie.get_suggestions("xyz") == []


def test_get_suggestions_zero_top_n_returns_empty() -> None:
    trie = Trie()
    trie.insert("apel", 10)
    assert trie.get_suggestions("ap", 0) == []


def test_get_suggestions_rejects_negative_top_n() -> None:
    trie = Trie()
    trie.insert("apel", 10)
    with pytest.raises(ValueError):
        trie.get_suggestions("ap", -1)


def test_get_suggestions_rejects_invalid_top_n_type() -> None:
    trie = Trie()
    trie.insert("apel", 10)
    with pytest.raises(TypeError):
        trie.get_suggestions("ap", 1.5)
    with pytest.raises(TypeError):
        trie.get_suggestions("ap", True)


def test_empty_word_is_rejected() -> None:
    trie = Trie()
    with pytest.raises(ValueError):
        trie.insert("", 10)
    with pytest.raises(ValueError):
        trie.insert("   ", 10)


def test_invalid_word_type_is_rejected() -> None:
    trie = Trie()
    with pytest.raises(TypeError):
        trie.insert(123, 10)


def test_invalid_frequency_is_rejected() -> None:
    trie = Trie()
    with pytest.raises(ValueError):
        trie.insert("apel", -1)
    with pytest.raises(TypeError):
        trie.insert("apel", 1.5)


def test_boolean_frequency_is_rejected() -> None:
    trie = Trie()
    with pytest.raises(TypeError):
        trie.insert("apel", True)


def test_invalid_prefix_type_is_rejected() -> None:
    trie = Trie()
    with pytest.raises(TypeError):
        trie.starts_with(123)
    with pytest.raises(TypeError):
        trie.get_suggestions(123)


def test_search_invalid_word_type_is_rejected() -> None:
    trie = Trie()
    with pytest.raises(TypeError):
        trie.search(123)


def test_iter_words_returns_all_words_sorted() -> None:
    trie = Trie()
    trie.insert("rumah", 100)
    trie.insert("rumput", 80)
    trie.insert("roti", 50)
    assert list(trie.iter_words()) == [
        ("roti", 50),
        ("rumah", 100),
        ("rumput", 80),
    ]


def test_iter_words_returns_prefix_word_and_descendants() -> None:
    trie = Trie()
    trie.insert("api", 30)
    trie.insert("aplikasi", 50)
    trie.insert("ap", 10)
    assert list(trie.iter_words()) == [
        ("ap", 10),
        ("api", 30),
        ("aplikasi", 50),
    ]


def test_indonesian_characters_are_supported() -> None:
    trie = Trie()
    trie.insert("café", 10)
    trie.insert("anak-anak", 20)
    trie.insert("buku", 30)
    assert trie.search("CAFÉ") is True
    assert trie.search("anak-anak") is True
    assert trie.get_suggestions("an") == [("anak-anak", 20)]


def test_insert_duplicate_word_edge_case() -> None:
    trie = Trie()
    trie.insert("kata", 5)
    trie.insert("kata", 10)
    assert trie.word_count == 1
    assert trie.search("kata") is True
    assert trie.get_suggestions("ka") == [("kata", 10)]


def test_starts_with_prefix_is_prefix_of_word() -> None:
    trie = Trie()
    trie.insert("programming", 100)
    assert trie.starts_with("prog") is True
    assert trie.starts_with("program") is True
    assert trie.starts_with("programming") is True


def test_starts_with_prefix_not_prefix() -> None:
    trie = Trie()
    trie.insert("programming", 100)
    assert trie.starts_with("pro") is True
    assert trie.starts_with("pr") is True
    assert trie.starts_with("p") is True
    assert trie.starts_with("x") is False


def test_starts_with_empty_prefix_returns_true() -> None:
    trie = Trie()
    trie.insert("program", 100)
    assert trie.starts_with("") is True
    assert trie.starts_with("   ") is True


def test_search_word_not_exact_match() -> None:
    trie = Trie()
    trie.insert("programming", 100)
    assert trie.search("program") is False
    assert trie.search("programming") is True


def test_get_suggestions_with_multiple_words_same_frequency() -> None:
    trie = Trie()
    trie.insert("apel", 10)
    trie.insert("api", 10)
    trie.insert("aplikasi", 10)
    results = trie.get_suggestions("ap")
    assert len(results) == 3
    assert results == [("apel", 10), ("api", 10), ("aplikasi", 10)]