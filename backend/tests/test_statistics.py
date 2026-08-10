from app.core.trie import Trie
from app.utils.statistics import (
    ESTIMATED_NODE_SIZE_BYTES,
    calculate_average_depth,
    estimate_memory_bytes,
    estimate_memory_megabytes,
)


def test_average_depth() -> None:
    trie = Trie()

    trie.insert("a", 10)
    trie.insert("ab", 20)
    trie.insert("abc", 30)

    assert calculate_average_depth(trie) == 2.0


def test_average_depth_with_shared_prefix() -> None:
    trie = Trie()

    trie.insert("apel", 10)
    trie.insert("api", 20)

    expected = (4 + 3) / 2

    assert calculate_average_depth(trie) == expected


def test_average_depth_for_empty_trie() -> None:
    trie = Trie()

    assert calculate_average_depth(trie) == 0.0


def test_memory_estimate_bytes() -> None:
    trie = Trie()

    trie.insert("apel", 10)

    assert estimate_memory_bytes(trie) == (
        trie.node_count * ESTIMATED_NODE_SIZE_BYTES
    )


def test_memory_estimate_megabytes() -> None:
    trie = Trie()

    trie.insert("apel", 10)

    expected_bytes = estimate_memory_bytes(trie)
    expected_megabytes = expected_bytes / (1024 * 1024)

    assert estimate_memory_megabytes(trie) == expected_megabytes


def test_statistics_change_with_trie_size() -> None:
    small_trie = Trie()
    large_trie = Trie()

    small_trie.insert("apel", 10)

    large_trie.insert("apel", 10)
    large_trie.insert("aplikasi", 20)
    large_trie.insert("komputer", 30)

    assert large_trie.word_count > small_trie.word_count
    assert large_trie.node_count > small_trie.node_count
    assert estimate_memory_bytes(large_trie) > estimate_memory_bytes(
        small_trie
    )