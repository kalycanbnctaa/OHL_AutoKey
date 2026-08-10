from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DictionaryEntry:
    word: str
    frequency: int