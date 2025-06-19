import requests
from datetime import datetime

API_KEY = "b8c32597-22d2-4fb6-b5cf-03a66f841f46"
API_URL = "https://newsapi.ai/api/v1/article/getArticles"

def get_tech_news(count=5):
    payload = {
        "action": "getArticles",
        "keyword": "technology",
        "articlesPage": 1,
        "articlesCount": count,
        "resultType": "articles",
        "sortBy": "date",
        "lang": "eng",
        "apiKey": API_KEY,
    }

    try:
        res = requests.post(API_URL, json=payload, timeout=5)
        res.raise_for_status()
        articles = res.json().get("articles", {}).get("results", [])

        if not articles:
            return "❌ No tech news found."

        result = f"📰 Latest Tech News (as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):\n\n"
        for art in articles:
            title = art.get("title", "No title")
            url = art.get("url", "")
            result += f"• {title}\n  {url}\n\n"

        return result.strip()

    except Exception as e:
        return f"⚠️ Error fetching news: {e}"