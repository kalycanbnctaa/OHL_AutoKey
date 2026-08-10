import math
from app.core.knapsack import solve_knapsack, KnapsackResult
from app.services.dictionary_service import DictionaryService

class SmartTrimService:
    def __init__(self, dictionary_service: DictionaryService):
        self.dictionary_service = dictionary_service

    def trim(self, text: str, limit: int) -> KnapsackResult | None:
        if not text or limit <= 0:
            return None

        words = text.split()
        if not words:
            return None

        total_freq = self.dictionary_service.total_frequency
        if total_freq <= 0:
            return None

        items: list[tuple[str, int, float]] = []
        for word in words:
            entry = self.dictionary_service.search(word)
            if entry is None:
                continue
            freq = max(entry.frequency, 1)
            weight = len(word)
            value = math.log(total_freq / freq)
            items.append((word, weight, value))

        if not items:
            return None

        return solve_knapsack(items, limit)