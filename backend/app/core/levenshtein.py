from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LevenshteinTable:
    source: str
    target: str
    table: list[list[int]]
    distance: int


def _validate_strings(source: str, target: str) -> None:
    if not isinstance(source, str) or not isinstance(target, str):
        raise TypeError("source and target must be strings")


def compute_distance_table(source: str, target: str) -> LevenshteinTable:
    _validate_strings(source, target)

    n = len(source)
    m = len(target)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i

    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if source[i - 1] == target[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )

    return LevenshteinTable(
        source=source,
        target=target,
        table=dp,
        distance=dp[n][m],
    )


def levenshtein_distance(source: str, target: str) -> int:
    _validate_strings(source, target)

    n = len(source)
    m = len(target)

    previous_row = list(range(m + 1))

    for i in range(1, n + 1):
        current_row = [i] + [0] * m

        for j in range(1, m + 1):
            cost = 0 if source[i - 1] == target[j - 1] else 1

            current_row[j] = min(
                previous_row[j] + 1,
                current_row[j - 1] + 1,
                previous_row[j - 1] + cost,
            )

        previous_row = current_row

    return previous_row[m]