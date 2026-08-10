import pytest

from app.core.bigram import BigramCounts
from app.services.bigram_service import BigramService

def test_bigram_counts_add_pair():
    bc = BigramCounts()
    bc.add_pair("data", "science")
    bc.add_pair("data", "science")
    bc.add_pair("data", "analysis")
    assert bc.total_pairs == 3
    assert bc.get_count("data", "science") == 2
    assert bc.get_count("data", "analysis") == 1
    assert bc.get_total_for_prev("data") == 3

def test_bigram_counts_add_pair_ignores_empty():
    bc = BigramCounts()
    bc.add_pair("", "science")
    bc.add_pair("data", "")
    bc.add_pair("", "")
    assert bc.total_pairs == 0
    assert bc.get_count("data", "science") == 0

def test_bigram_counts_probability():
    bc = BigramCounts()
    bc.add_pair("data", "science")
    bc.add_pair("data", "science")
    bc.add_pair("data", "analysis")
    assert bc.probability("data", "science") == pytest.approx(2/3)
    assert bc.probability("data", "analysis") == pytest.approx(1/3)
    assert bc.probability("data", "unknown") == 0.0
    assert bc.probability("unknown", "science") == 0.0

def test_bigram_counts_get_total_for_prev_unknown():
    bc = BigramCounts()
    assert bc.get_total_for_prev("unknown") == 0

def test_bigram_service_record_and_rerank():
    svc = BigramService()
    session_id = "test-session"
    svc.record_pair(session_id, "data", "science")
    svc.record_pair(session_id, "data", "science")
    svc.record_pair(session_id, "data", "analysis")

    candidates = [("science", 100), ("analysis", 200), ("program", 50)]
    scored = svc.rerank_suggestions(session_id, "data", candidates)

    assert scored[0][0] in ("science", "analysis")
    assert scored[-1][0] == "program"

def test_bigram_service_rerank_no_data():
    svc = BigramService()
    session_id = "test-session"
    candidates = [("science", 100), ("analysis", 200)]
    scored = svc.rerank_suggestions(session_id, "data", candidates)
    assert scored == [("analysis", 200, 0.0), ("science", 100, 0.0)]

def test_bigram_service_rerank_unknown_prev():
    svc = BigramService()
    session_id = "test-session"
    svc.record_pair(session_id, "data", "science")
    candidates = [("science", 100), ("analysis", 200)]
    scored = svc.rerank_suggestions(session_id, "unknown", candidates)
    assert scored == [("analysis", 200, 0.0), ("science", 100, 0.0)]

def test_bigram_service_rerank_empty_session():
    svc = BigramService()
    session_id = "nonexistent"
    candidates = [("science", 100)]
    scored = svc.rerank_suggestions(session_id, "data", candidates)
    assert scored == [("science", 100, 0.0)]

def test_bigram_service_statistics():
    svc = BigramService()
    session_id = "test-session"
    stats = svc.get_statistics(session_id)
    assert stats["total_pairs"] == 0
    assert stats["unique_pairs"] == 0

    svc.record_pair(session_id, "a", "b")
    svc.record_pair(session_id, "a", "c")
    stats = svc.get_statistics(session_id)
    assert stats["total_pairs"] == 2
    assert stats["unique_pairs"] == 2

def test_bigram_service_record_invalid_words():
    svc = BigramService()
    session_id = "test-session"
    svc.record_pair(session_id, "", "b")
    svc.record_pair(session_id, "a", "")
    stats = svc.get_statistics(session_id)
    assert stats["total_pairs"] == 0

def test_bigram_service_get_or_create_session():
    svc = BigramService()
    session = svc.get_or_create_session("test-id")
    assert session.session_id == "test-id"
    session2 = svc.get_or_create_session("test-id")
    assert session is session2

    session3 = svc.get_or_create_session()
    assert session3.session_id is not None
    assert len(session3.session_id) > 0

def test_bigram_counts_probability_with_zero_total():
    bc = BigramCounts()
    assert bc.probability("any", "word") == 0.0

def test_bigram_counts_get_count_unknown():
    bc = BigramCounts()
    assert bc.get_count("unknown", "word") == 0