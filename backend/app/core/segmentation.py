import math
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True, slots=True)
class SegmentationResult:
    text: str
    dp: list[float]
    choices: list[int]
    words: list[str]
    result: str
    cost: float

def segment_text(
    text: str,
    word_freq: dict[str, int],
    total_frequency: int,
) -> Optional[SegmentationResult]:
    if not text:
        return None

    n = len(text)
    INF = float("inf")
    dp = [INF] * (n + 1)
    choice = [-1] * (n + 1)
    dp[0] = 0.0

    for i in range(1, n + 1):
        for j in range(i):
            substring = text[j:i]
            freq = word_freq.get(substring)
            if freq is None or freq <= 0:
                continue
            cost = math.log(total_frequency / freq)
            if dp[j] + cost < dp[i]:
                dp[i] = dp[j] + cost
                choice[i] = j

    if dp[n] == INF:
        return None

    words = []
    i = n
    while i > 0:
        j = choice[i]
        words.append(text[j:i])
        i = j
    words.reverse()

    return SegmentationResult(
        text=text,
        dp=dp,
        choices=choice,
        words=words,
        result=" ".join(words),
        cost=dp[n],
    )