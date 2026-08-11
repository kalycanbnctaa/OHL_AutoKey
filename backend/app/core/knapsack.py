from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True, slots=True)
class KnapsackResult:
    items: list[tuple[str, int, float]]
    total_value: float
    total_weight: int
    selected_indices: list[int]
    dp_table: list[list[float]]

def solve_knapsack(
    items: list[tuple[str, int, float]],
    capacity: int,
) -> Optional[KnapsackResult]:
    if not items:
        return None

    n = len(items)
    dp = [[0.0] * (capacity + 1) for _ in range(n + 1)]
    keep = [[False] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        _, weight, value = items[i - 1]
        for w in range(capacity + 1):
            if weight <= w and dp[i - 1][w - weight] + value > dp[i - 1][w]:
                dp[i][w] = dp[i - 1][w - weight] + value
                keep[i][w] = True
            else:
                dp[i][w] = dp[i - 1][w]
                keep[i][w] = False

    total_value = dp[n][capacity]
    selected_indices: list[int] = []
    w = capacity
    for i in range(n, 0, -1):
        if keep[i][w]:
            selected_indices.append(i - 1)
            w -= items[i - 1][1]

    selected_indices.reverse()
    selected_items = [items[i] for i in selected_indices]

    return KnapsackResult(
        items=selected_items,
        total_value=total_value,
        total_weight=sum(item[1] for item in selected_items),
        selected_indices=selected_indices,
        dp_table=dp,
    )