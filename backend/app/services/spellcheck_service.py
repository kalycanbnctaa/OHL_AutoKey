import re
from dataclasses import dataclass

from app.core.levenshtein import levenshtein_distance
from app.services.dictionary_service import DictionaryService

DEFAULT_MAX_DISTANCE = 2
MAX_ALLOWED_DISTANCE = 5
DEFAULT_TOP_N = 5

_WORD_PATTERN = re.compile(r"[a-zA-Z0-9\u00C0-\u024F'-]+")

@dataclass(frozen=True, slots=True)
class SpellCheckCandidate:
    word: str
    distance: int
    frequency: int

@dataclass(frozen=True, slots=True)
class SpellCheckIssue:
    word: str
    start: int
    end: int
    suggestions: list[SpellCheckCandidate]

def tokenize(text: str) -> list[tuple[str, int, int]]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    return [(match.group(), match.start(), match.end()) for match in _WORD_PATTERN.finditer(text)]

class SpellCheckService:
    def __init__(self, dictionary_service: DictionaryService) -> None:
        self.dictionary_service = dictionary_service

    def is_valid_word(self, word: str) -> bool:
        if not isinstance(word, str):
            raise TypeError("Word must be a string")

        normalized = word.strip().lower()

        if not normalized:
            return False

        return self.dictionary_service.search(normalized) is not None

    def find_words_within_distance(
        self,
        word: str,
        max_distance: int = DEFAULT_MAX_DISTANCE,
        limit: int | None = None,
    ) -> list[SpellCheckCandidate]:
        if not isinstance(word, str):
            raise TypeError("Word must be a string")

        if isinstance(max_distance, bool) or not isinstance(max_distance, int):
            raise TypeError("max_distance must be an integer")

        if max_distance < 0:
            raise ValueError("max_distance must not be negative")

        if max_distance > MAX_ALLOWED_DISTANCE:
            raise ValueError(
                f"max_distance must not exceed {MAX_ALLOWED_DISTANCE}"
            )

        if limit is not None:
            if isinstance(limit, bool) or not isinstance(limit, int):
                raise TypeError("limit must be an integer")

            if limit < 0:
                raise ValueError("limit must not be negative")

        normalized_word = word.strip().lower()

        if not normalized_word:
            return []

        candidates: list[SpellCheckCandidate] = []
        word_length = len(normalized_word)

        for entry_word, entry in self.dictionary_service.entries.items():
            if abs(len(entry_word) - word_length) > max_distance:
                continue

            distance = levenshtein_distance(normalized_word, entry_word)

            if distance <= max_distance:
                candidates.append(
                    SpellCheckCandidate(
                        word=entry_word,
                        distance=distance,
                        frequency=entry.frequency,
                    )
                )

        candidates.sort(key=lambda candidate: (candidate.distance, -candidate.frequency, candidate.word))

        if limit is not None:
            return candidates[:limit]

        return candidates

    def check_text(
        self,
        text: str,
        max_distance: int = DEFAULT_MAX_DISTANCE,
        top_n: int = DEFAULT_TOP_N,
    ) -> list[SpellCheckIssue]:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        issues: list[SpellCheckIssue] = []

        for word, start, end in tokenize(text):
            normalized = word.lower()

            if normalized.isdigit():
                continue

            if self.dictionary_service.search(normalized) is not None:
                continue

            suggestions = self.find_words_within_distance(
                normalized, max_distance=max_distance, limit=top_n
            )

            issues.append(
                SpellCheckIssue(
                    word=word,
                    start=start,
                    end=end,
                    suggestions=suggestions,
                )
            )

        return issues