from fastapi.testclient import TestClient

from app.main import app

def test_root() -> None:
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "application": "AutoKey",
        "version": "0.1.0",
        "status": "ok",
    }

def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_statistics() -> None:
    with TestClient(app) as client:
        response = client.get("/statistics")
    assert response.status_code == 200
    data = response.json()
    assert set(data) == {
        "word_count",
        "node_count",
        "average_depth",
        "memory_bytes",
        "memory_megabytes",
    }
    assert data["word_count"] > 0
    assert data["node_count"] >= data["word_count"]
    assert data["average_depth"] > 0
    assert data["memory_bytes"] > 0
    assert data["memory_megabytes"] > 0

def test_autocomplete_returns_ranked_suggestions() -> None:
    with TestClient(app) as client:
        response = client.get("/autocomplete", params={"prefix": "prog"})
    assert response.status_code == 200
    data = response.json()
    assert data["prefix"] == "prog"
    assert isinstance(data["latency_ms"], float)
    assert len(data["suggestions"]) <= 5
    frequencies = [item["frequency"] for item in data["suggestions"]]
    assert frequencies == sorted(frequencies, reverse=True)

def test_autocomplete_respects_top_n() -> None:
    with TestClient(app) as client:
        response = client.get("/autocomplete", params={"prefix": "a", "top_n": 3})
    assert response.status_code == 200
    assert len(response.json()["suggestions"]) <= 3

def test_autocomplete_unknown_prefix_returns_empty() -> None:
    with TestClient(app) as client:
        response = client.get("/autocomplete", params={"prefix": "zzzzzzzzzz"})
    assert response.status_code == 200
    assert response.json()["suggestions"] == []

def test_autocomplete_empty_prefix_returns_empty() -> None:
    with TestClient(app) as client:
        response = client.get("/autocomplete", params={"prefix": ""})
    assert response.status_code == 200
    assert response.json()["suggestions"] == []

def test_autocomplete_rejects_top_n_out_of_range() -> None:
    with TestClient(app) as client:
        response = client.get("/autocomplete", params={"prefix": "a", "top_n": 0})
    assert response.status_code == 422

def test_autocomplete_latency_is_fast() -> None:
    with TestClient(app) as client:
        response = client.get("/autocomplete", params={"prefix": "prog"})
    assert response.json()["latency_ms"] < 100

def test_spellcheck_word_valid() -> None:
    with TestClient(app) as client:
        response = client.get("/spellcheck/word", params={"word": "makan"})
    assert response.status_code == 200
    data = response.json()
    assert data["word"] == "makan"
    assert data["is_valid"] is True
    assert isinstance(data["suggestions"], list)

def test_spellcheck_word_unknown_returns_ranked_suggestions() -> None:
    with TestClient(app) as client:
        response = client.get("/spellcheck/word", params={"word": "kalimt", "max_distance": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is False
    distances = [item["distance"] for item in data["suggestions"]]
    assert distances == sorted(distances)
    assert all(d <= 2 for d in distances)

def test_spellcheck_word_respects_top_n() -> None:
    with TestClient(app) as client:
        response = client.get("/spellcheck/word", params={"word": "kalimt", "top_n": 3})
    assert response.status_code == 200
    assert len(response.json()["suggestions"]) <= 3

def test_spellcheck_word_rejects_empty() -> None:
    with TestClient(app) as client:
        response = client.get("/spellcheck/word", params={"word": ""})
    assert response.status_code == 422

def test_levenshtein_table_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/levenshtein/table", params={"source": "kitten", "target": "sitting"})
    assert response.status_code == 200
    data = response.json()
    assert data["distance"] == 3
    assert len(data["table"]) == 7
    assert len(data["table"][0]) == 8

def test_levenshtein_table_empty_strings() -> None:
    with TestClient(app) as client:
        response = client.get("/levenshtein/table", params={"source": "", "target": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["distance"] == 0
    assert len(data["table"]) == 1
    assert len(data["table"][0]) == 1

def test_spellcheck_check_text() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/spellcheck/check-text",
            json={"text": "saya sedang menuliss sebuah kalimt"},
        )
    assert response.status_code == 200
    data = response.json()
    flagged_words = [issue["word"] for issue in data["issues"]]
    assert "menuliss" in flagged_words
    assert "kalimt" in flagged_words
    assert data["issue_count"] == len(data["issues"])

def test_spellcheck_check_text_empty() -> None:
    with TestClient(app) as client:
        response = client.post("/spellcheck/check-text", json={"text": ""})
    assert response.status_code == 200
    assert response.json()["issues"] == []

def test_segment_endpoint_success() -> None:
    with TestClient(app) as client:
        response = client.post("/segment", json={"text": "programdinamis"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["result"] == "program dinamis"
    assert data["words"] == ["program", "dinamis"]
    assert data["dp"][0] == 0.0
    assert data["dp"][-1] == data["cost"]

def test_segment_endpoint_failure() -> None:
    with TestClient(app) as client:
        response = client.post("/segment", json={"text": "xyz"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "error" in data
    assert data["error"] is not None

def test_segment_endpoint_empty_text() -> None:
    with TestClient(app) as client:
        response = client.post("/segment", json={"text": ""})
    assert response.status_code == 422

def test_smart_trim_endpoint_success() -> None:
    with TestClient(app) as client:
        response = client.post("/smart-trim", json={"text": "program dinamis", "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_weight"] <= 10
    assert len(data["items"]) >= 1

def test_smart_trim_endpoint_invalid_words() -> None:
    with TestClient(app) as client:
        response = client.post("/smart-trim", json={"text": "xyz zzz", "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"] is not None

def test_dictionary_add_word() -> None:
    with TestClient(app) as client:
        response = client.get("/spellcheck/word", params={"word": "newword"})
        assert response.json()["is_valid"] is False

        response = client.post("/dictionary/add", json={"word": "newword"})
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.json()["word"] == "newword"

        response = client.get("/spellcheck/word", params={"word": "newword"})
        assert response.json()["is_valid"] is True

def test_bigram_record_pair() -> None:
    with TestClient(app) as client:
        headers = {"X-Session-Id": "test-session"}
        response = client.post(
            "/bigram/record",
            json={"prev": "data", "curr": "science"},
            headers=headers,
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_pairs"] == 1
    assert data["unique_pairs"] == 1

def test_bigram_record_pair_no_session() -> None:
    with TestClient(app) as client:
        response = client.post("/bigram/record", json={"prev": "data", "curr": "science"})
    assert response.status_code == 400
    assert "X-Session-Id" in response.text

def test_bigram_statistics() -> None:
    with TestClient(app) as client:
        headers = {"X-Session-Id": "test-session-2"}
        response = client.get("/bigram/statistics", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_pairs"] == 0
    assert data["unique_pairs"] == 0

    client.post(
        "/bigram/record",
        json={"prev": "data", "curr": "analysis"},
        headers=headers,
    )
    response = client.get("/bigram/statistics", headers=headers)
    data = response.json()
    assert data["total_pairs"] == 1
    assert data["unique_pairs"] == 1

def test_cors_allows_configured_frontend() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"},
        )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"