import uuid
from app.models.session import Session
from app.core.bigram import BigramCounts

class BigramService:
    def __init__(self):
        self.sessions: dict[str, Session] = {}

    def get_or_create_session(self, session_id: str | None = None) -> Session:
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]
        new_id = session_id or str(uuid.uuid4())
        session = Session(session_id=new_id)
        self.sessions[new_id] = session
        return session

    def record_pair(self, session_id: str, prev: str, curr: str) -> None:
        if not prev or not curr:
            return
        session = self.get_or_create_session(session_id)
        session.bigram.add_pair(prev, curr)
        session.last_word = curr

    def get_counts(self, session_id: str) -> BigramCounts | None:
        session = self.sessions.get(session_id)
        return session.bigram if session else None

    def rerank_suggestions(
        self,
        session_id: str,
        prev_word: str,
        candidates: list[tuple[str, int]],
    ) -> list[tuple[str, int, float]]:
        session = self.sessions.get(session_id)
        if not session or not prev_word:
            sorted_candidates = sorted(candidates, key=lambda x: (-x[1], x[0]))
            return [(word, freq, 0.0) for word, freq in sorted_candidates]

        bigram = session.bigram
        scored = []
        for word, freq in candidates:
            prob = bigram.probability(prev_word, word)
            score = prob * freq
            scored.append((word, freq, score))

        scored.sort(key=lambda x: (-x[2], -x[1], x[0]))
        return scored

    def get_statistics(self, session_id: str) -> dict:
        session = self.sessions.get(session_id)
        if not session:
            return {"total_pairs": 0, "unique_pairs": 0}
        return {
            "total_pairs": session.bigram.total_pairs,
            "unique_pairs": len(session.bigram.counts),
        }