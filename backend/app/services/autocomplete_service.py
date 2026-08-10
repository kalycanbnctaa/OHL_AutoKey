from app.models.dictionary_entry import DictionaryEntry
from app.services.dictionary_service import DictionaryService

DEFAULT_TOP_N = 5
MAX_TOP_N = 20


class AutocompleteService:
    def __init__(self, dictionary_service: DictionaryService) -> None:
        self.dictionary_service = dictionary_service

    def get_suggestions(
        self,
        prefix: str,
        top_n: int = DEFAULT_TOP_N,
    ) -> list[DictionaryEntry]:
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be a string")

        normalized_prefix = prefix.strip()

        if not normalized_prefix:
            return []

        if top_n <= 0:
            return []

        bounded_top_n = min(top_n, MAX_TOP_N)

        return self.dictionary_service.get_suggestions(
            normalized_prefix, bounded_top_n
        )