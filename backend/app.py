import config
from config import STUDENT_ID
import feedparser
	
# ... існуючі імпорти і код ...
	
# Пам'ять для статей (словник: student_id -> список статей)
news_store = {STUDENT_ID: []}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import STUDENT_ID, SOURCES
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STUDENT_ID = "Apostolov_47b86c25"

fake_users_db = {
    STUDENT_ID: {
        "username": STUDENT_ID,
        "full_name": STUDENT_ID,
        "hashed_password": "1488911",  # НЕ рекомендується зберігати пароль так у продакшені
        "disabled": False,
    }
}

# Пам'ять для збереження джерел (для кожного STUDENT_ID окремо)
store = {STUDENT_ID: SOURCES.copy()}

@app.get("/sources/{student_id}")
def get_sources(student_id: str):
    if student_id not in store:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"sources": store[student_id]}

@app.post("/sources/{student_id}")
def add_source(student_id: str, payload: dict):
    if student_id != STUDENT_ID:
        raise HTTPException(status_code=404, detail="Student not found")
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    store[student_id].append(url)
    return {"sources": store[student_id]}

@app.post("/fetch/{student_id}")
def fetch_news(student_id: str):
    if student_id != STUDENT_ID:
        raise HTTPException(status_code=404, detail="Student not found")
    # Очищаємо попередній кеш
    news_store[student_id].clear()
    fetched = 0
    for url in config.SOURCES:
        feed = feedparser.parse(url)
        for entry in getattr(feed, "entries", []):
            news_store[student_id].append({
                "title": entry.get("title", ""),
                "link":  entry.get("link", ""),
                "published": entry.get("published", "")
            })
            fetched += 1
    return {"fetched": fetched}

@app.get("/news/{student_id}")
def get_news(student_id: str):
    if student_id not in news_store:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"articles": news_store[student_id]}

analyzer = SentimentIntensityAnalyzer()
@app.post("/analyze/{student_id}")
def analyze_tone(student_id: str):
    if student_id != STUDENT_ID:
        raise HTTPException(status_code=404, detail="Student not found")
    articles = news_store.get(student_id, [])
    result = []
    for art in articles:
        text = art.get("title", "")
        scores = analyzer.polarity_scores(text)
        comp = scores["compound"]
        if comp >= 0.05:
            label = "positive"
        elif comp <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        # Додаємо поля "sentiment" і "scores" в копію статті
        result.append({**art, "sentiment": label, "scores": scores})
    return {"analyzed": len(result), "articles": result}
