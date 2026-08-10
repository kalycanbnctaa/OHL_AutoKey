from dataclasses import dataclass, field
from app.core.bigram import BigramCounts

@dataclass
class Session:
    session_id: str
    bigram: BigramCounts = field(default_factory=BigramCounts)
    last_word: str | None = None