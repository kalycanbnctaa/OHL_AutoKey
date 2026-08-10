from collections.abc import Iterator
import heapq

from app.models.trie_node import TrieNode


class _SuggestionCandidate:
    __slots__ = ("key", "word", "frequency")

    def __init__(self, key: tuple[int, str], word: str, frequency: int) -> None:
        self.key = key
        self.word = word
        self.frequency = frequency

    def __lt__(self, other: "_SuggestionCandidate") -> bool:
        return self.key > other.key


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()
        self.word_count = 0
        self.node_count = 1

    @staticmethod
    def _normalize_word(word: str) -> str:
        if not isinstance(word, str):
            raise TypeError("Word must be a string")

        normalized = word.strip().lower()

        if not normalized:
            raise ValueError("Word must not be empty")

        return normalized

    @staticmethod
    def _normalize_prefix(prefix: str) -> str:
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be a string")

        return prefix.strip().lower()

    @staticmethod
    def _validate_frequency(frequency: int) -> None:
        if isinstance(frequency, bool) or not isinstance(frequency, int):
            raise TypeError("Frequency must be an integer")

        if frequency < 0:
            raise ValueError("Frequency must not be negative")

    @staticmethod
    def _validate_top_n(top_n: int) -> None:
        if isinstance(top_n, bool) or not isinstance(top_n, int):
            raise TypeError("top_n must be an integer")

        if top_n < 0:
            raise ValueError("top_n must not be negative")

    def insert(self, word: str, frequency: int) -> None:
        normalized_word = self._normalize_word(word)
        self._validate_frequency(frequency)

        node = self.root

        for char in normalized_word:
            child = node.children.get(char)

            if child is None:
                child = TrieNode()
                node.children[char] = child
                self.node_count += 1

            node = child

        if not node.is_word:
            self.word_count += 1

        node.is_word = True
        node.frequency = frequency

    def search(self, word: str) -> bool:
        normalized_word = self._normalize_word(word)
        node = self._find_node(normalized_word)

        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        normalized_prefix = self._normalize_prefix(prefix)

        if not normalized_prefix:
            return True

        return self._find_node(normalized_prefix) is not None

    def get_suggestions(
        self,
        prefix: str,
        top_n: int = 5,
    ) -> list[tuple[str, int]]:
        self._validate_top_n(top_n)

        if top_n == 0:
            return []

        normalized_prefix = self._normalize_prefix(prefix)
        node = self._find_node(normalized_prefix)

        if node is None:
            return []

        heap: list[_SuggestionCandidate] = []
        self._collect_top_k(node, normalized_prefix, top_n, heap)
        heap.sort(key=lambda candidate: candidate.key)

        return [(candidate.word, candidate.frequency) for candidate in heap]

    def iter_words(self) -> Iterator[tuple[str, int]]:
        yield from self._iter_node(self.root, "")

    def _iter_node(
        self,
        node: TrieNode,
        prefix: str,
    ) -> Iterator[tuple[str, int]]:
        if node.is_word:
            yield prefix, node.frequency

        for char in sorted(node.children):
            yield from self._iter_node(node.children[char], prefix + char)

    def _find_node(self, text: str) -> TrieNode | None:
        node = self.root

        for char in text:
            node = node.children.get(char)

            if node is None:
                return None

        return node

    def _collect_top_k(
        self,
        node: TrieNode,
        prefix: str,
        top_n: int,
        heap: list["_SuggestionCandidate"],
    ) -> None:
        if node.is_word:
            key = (-node.frequency, prefix)

            if len(heap) < top_n:
                heapq.heappush(
                    heap, _SuggestionCandidate(key, prefix, node.frequency)
                )
            elif key < heap[0].key:
                heapq.heapreplace(
                    heap, _SuggestionCandidate(key, prefix, node.frequency)
                )

        for char in sorted(node.children):
            self._collect_top_k(node.children[char], prefix + char, top_n, heap)