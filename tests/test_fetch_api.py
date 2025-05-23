from fastapi.testclient import TestClient
from backend.app import app, news_store
from config import STUDENT_ID
import feedparser

client = TestClient(app)

def test_get_news_empty():
    # Порожній початковий стан
    news_store[STUDENT_ID] = []
    res = client.get(f"/news/{STUDENT_ID}")
    assert res.status_code == 200
    assert res.json() == {"articles": []}

class DummyFeed:
    entries = [
        {"title": "T1", "link": "<http://a>", "published": "2025-01-01"},
        {"title": "T2", "link": "<http://b>", "published": ""}
    ]

def test_fetch_and_get(monkeypatch):
    # Змінюємо SOURCES у модулі config
    monkeypatch.setattr("config.SOURCES", ["<http://example.com/rss>"])
    # Підмінюємо функцію parse, щоб не робити реальний HTTP-запит
    monkeypatch.setattr(feedparser, "parse", lambda url: DummyFeed)
    news_store[STUDENT_ID] = []
    res1 = client.post(f"/fetch/{STUDENT_ID}")
    assert res1.status_code == 200
    assert res1.json() == {"fetched": 2}
    res2 = client.get(f"/news/{STUDENT_ID}")
    assert res2.status_code == 200
    assert res2.json() == {
        "articles": [
            {"title": "T1", "link": "<http://a>", "published": "2025-01-01"},
            {"title": "T2", "link": "<http://b>", "published": ""}
        ]
    }
