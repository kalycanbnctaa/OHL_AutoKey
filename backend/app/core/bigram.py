from dataclasses import dataclass, field

@dataclass
class BigramCounts:
    counts: dict[tuple[str, str], int] = field(default_factory=dict)
    total_pairs: int = 0

    def add_pair(self, prev: str, curr: str) -> None:
        if not prev or not curr:
            return
        key = (prev, curr)
        self.counts[key] = self.counts.get(key, 0) + 1
        self.total_pairs += 1

    def get_count(self, prev: str, curr: str) -> int:
        return self.counts.get((prev, curr), 0)

    def get_total_for_prev(self, prev: str) -> int:
        return sum(cnt for (p, _), cnt in self.counts.items() if p == prev)

    def probability(self, prev: str, curr: str) -> float:
        total = self.get_total_for_prev(prev)
        if total == 0:
            return 0.0
        return self.get_count(prev, curr) / total