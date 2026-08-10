from app.core.trie import Trie
from app.models.trie_node import TrieNode

ESTIMATED_NODE_SIZE_BYTES = 96


def calculate_average_depth(trie: Trie) -> float:
    if trie.word_count == 0:
        return 0.0

    total_depth = 0
    word_count = 0
    stack: list[tuple[TrieNode, int]] = [(trie.root, 0)]

    while stack:
        node, depth = stack.pop()

        if node.is_word:
            total_depth += depth
            word_count += 1

        for child in node.children.values():
            stack.append((child, depth + 1))

    if word_count == 0:
        return 0.0

    return total_depth / word_count


def estimate_memory_bytes(trie: Trie) -> int:
    return trie.node_count * ESTIMATED_NODE_SIZE_BYTES


def estimate_memory_megabytes(trie: Trie) -> float:
    return estimate_memory_bytes(trie) / (1024 * 1024)