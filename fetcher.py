import requests, datetime, json, os
from dateutil import parser

class NewsFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch(self, query: str, limit: int = 10):
        """
        Fetch articles from NewsAPI.org (everything endpoint).
        Returns list of dicts with keys: title, publishedAt (ISO), content, url, source.
        """
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "pageSize": min(limit,100),
            "language": "en",
            "sortBy": "relevancy",
            "apiKey": self.api_key
        }
        resp = requests.get(url, params=params, timeout=20)
        data = resp.json()
        articles = []
        for a in data.get("articles", [])[:limit]:
            articles.append({
                "title": a.get("title"),
                "publishedAt": a.get("publishedAt"),
                "content": a.get("content") or a.get("description") or "",
                "url": a.get("url"),
                "source": a.get("source", {}).get("name")
            })
        return articles

def load_sample_articles(limit=10):
    here = os.path.dirname(__file__)
    sample_fn = os.path.join(here, "sample_articles.json")
    with open(sample_fn, "r", encoding="utf-8") as f:
        articles = json.load(f)
    return articles[:limit]
