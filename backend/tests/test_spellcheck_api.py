from fastapi.testclient import TestClient

from app.main import app


def test_spellcheck_word_valid() -> None:
    with TestClient(app) as client:
        response = client.get("/spellcheck/word", params={"word": "makan"})

    assert response.status_code == 200

    data = response.json()

    assert data["word"] == "makan"
    assert isinstance(data["is_valid"], bool)
    assert isinstance(data["suggestions"], list)


def test_spellcheck_word_unknown_returns_ranked_suggestions() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/spellcheck/word", params={"word": "kalimt", "max_distance": 2}
        )

    assert response.status_code == 200

    data = response.json()

    assert data["is_valid"] is False

    distances = [item["distance"] for item in data["suggestions"]]
    assert distances == sorted(distances)
    assert all(distance <= 2 for distance in distances)


def test_spellcheck_word_respects_top_n() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/spellcheck/word",
            params={"word": "kalimt", "max_distance": 2, "top_n": 3},
        )

    assert response.status_code == 200
    assert len(response.json()["suggestions"]) <= 3


def test_spellcheck_word_rejects_empty_word() -> None:
    with TestClient(app) as client:
        response = client.get("/spellcheck/word", params={"word": ""})

    assert response.status_code == 422


def test_levenshtein_table_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/levenshtein/table",
            params={"source": "kitten", "target": "sitting"},
        )

    assert response.status_code == 200

    data = response.json()

    assert data["distance"] == 3
    assert len(data["table"]) == 7
    assert len(data["table"][0]) == 8


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


def test_spellcheck_check_text_empty_returns_no_issues() -> None:
    with TestClient(app) as client:
        response = client.post("/spellcheck/check-text", json={"text": ""})

    assert response.status_code == 200
    assert response.json()["issues"] == []