import json
from pathlib import Path
from typing import Any

from app.config import KAMUS_PATH
from app.core.trie import Trie
from app.models.dictionary_entry import DictionaryEntry

class DictionaryService:
    def __init__(self, dictionary_path: Path | None = None) -> None:
        self.dictionary_path = dictionary_path or KAMUS_PATH
        self.trie = Trie()
        self.entries: dict[str, DictionaryEntry] = {}
        self.total_frequency = 0
        self.is_loaded = False

    def load(self) -> None:
        if not self.dictionary_path.exists():
            raise FileNotFoundError(
                f"Dictionary file not found: {self.dictionary_path}"
            )
        if not self.dictionary_path.is_file():
            raise ValueError(
                f"Dictionary path is not a file: {self.dictionary_path}"
            )
        try:
            with self.dictionary_path.open("r", encoding="utf-8") as file:
                raw_data: Any = json.load(file)
        except json.JSONDecodeError as exc:
            raise ValueError("Dictionary file contains invalid JSON") from exc
        except OSError as exc:
            raise OSError(
                f"Unable to read dictionary file: {self.dictionary_path}"
            ) from exc

        if not isinstance(raw_data, dict):
            raise ValueError("Dictionary data must be a JSON object")

        new_trie = Trie()
        new_entries: dict[str, DictionaryEntry] = {}
        new_total_frequency = 0

        for raw_word, raw_frequency in raw_data.items():
            if not isinstance(raw_word, str):
                raise ValueError("Dictionary words must be strings")
            normalized_word = raw_word.strip().lower()
            if not normalized_word:
                continue
            if (
                isinstance(raw_frequency, bool)
                or not isinstance(raw_frequency, int)
            ):
                raise ValueError(
                    f"Invalid frequency for word '{raw_word}'"
                )
            if raw_frequency < 0:
                raise ValueError(
                    f"Frequency must not be negative for word '{raw_word}'"
                )
            if normalized_word in new_entries:
                raise ValueError(
                    "Duplicate dictionary word after normalization: "
                    f"'{normalized_word}'"
                )
            entry = DictionaryEntry(
                word=normalized_word,
                frequency=raw_frequency,
            )
            new_entries[normalized_word] = entry
            new_trie.insert(normalized_word, raw_frequency)
            new_total_frequency += raw_frequency

        self.trie = new_trie
        self.entries = new_entries
        self.total_frequency = new_total_frequency
        self.is_loaded = True

    def add_word(self, word: str, frequency: int = 1) -> None:
        if not isinstance(word, str):
            raise TypeError("Word must be a string")
        normalized = word.strip().lower()
        if not normalized:
            raise ValueError("Word must not be empty")
        if isinstance(frequency, bool) or not isinstance(frequency, int):
            raise TypeError("Frequency must be an integer")
        if frequency < 0:
            raise ValueError("Frequency must not be negative")

        existing = self.entries.get(normalized)
        if existing is not None:
            old_freq = existing.frequency
            self.total_frequency += (frequency - old_freq)
            self.trie.insert(normalized, frequency)
            self.entries[normalized] = DictionaryEntry(normalized, frequency)
        else:
            self.total_frequency += frequency
            self.trie.insert(normalized, frequency)
            self.entries[normalized] = DictionaryEntry(normalized, frequency)

    @property
    def word_count(self) -> int:
        return self.trie.word_count

    @property
    def node_count(self) -> int:
        return self.trie.node_count

    def search(self, word: str) -> DictionaryEntry | None:
        if not isinstance(word, str):
            raise TypeError("Word must be a string")
        normalized_word = word.strip().lower()
        if not normalized_word:
            return None
        return self.entries.get(normalized_word)

    def starts_with(self, prefix: str) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be a string")
        return self.trie.starts_with(prefix)

    def get_suggestions(
        self,
        prefix: str,
        top_n: int = 5,
    ) -> list[DictionaryEntry]:
        suggestions = self.trie.get_suggestions(prefix, top_n)
        return [
            DictionaryEntry(word=word, frequency=frequency)
            for word, frequency in suggestions
        ]