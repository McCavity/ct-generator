import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_home_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_no_cache_header(client):
    response = client.get("/")
    assert response.headers["Cache-Control"] == "no-store"


def test_response_is_html(client):
    response = client.get("/")
    assert b"<!DOCTYPE html>" in response.data


def test_de_sentence_structure_present(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "plant" in html
    assert "mit Hilfe von" in html


def test_en_sentence_structure_present(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "is plotting" in html
    assert "with the help of" in html


def test_disclaimer_present(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "This is fiction, not facts" in html
    assert "Dr. Axel Stoll" in html


def test_theme_class_applied(client):
    themes = [
        "theme-purple", "theme-red", "theme-blue", "theme-green",
        "theme-yellow", "theme-magenta", "theme-cyan", "theme-black",
    ]
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert any(t in html for t in themes)


def test_each_request_can_produce_different_theme(client):
    """Rolling 20 times should produce at least 2 distinct themes."""
    themes_seen = set()
    for _ in range(20):
        response = client.get("/")
        html = response.data.decode("utf-8")
        for t in ("theme-purple", "theme-red", "theme-blue", "theme-green",
                  "theme-yellow", "theme-magenta", "theme-cyan", "theme-black"):
            if t in html:
                themes_seen.add(t)
                break
    assert len(themes_seen) > 1, "All 20 requests returned the same theme — randomness broken"


def test_de_dice_values_in_response(client):
    """Response must contain at least one known DE d2 prefix."""
    known_prefixes = ["Finanz-", "Pharma-", "Alien-", "Medien-", "UFO-"]
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert any(p in html for p in known_prefixes)


def test_en_dice_values_in_response(client):
    """Response must contain at least one known EN d2 prefix."""
    known_prefixes = ["Finance-", "Pharma-", "Alien-", "Media-", "UFO-"]
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert any(p in html for p in known_prefixes)
