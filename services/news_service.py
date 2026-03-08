import os
import requests
from datetime import datetime, timedelta

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"
EVERYTHING_URL = "https://newsapi.org/v2/everything"

CACHE_DURATION = timedelta(minutes=30)
_cache = {"timestamp": None, "data": {}}

def get_news(category=None, country="us", limit=10, language="en"):
    global _cache
    
    cache_key = f"{category or 'general'}_fresh"
    
    # Return cached data if available
    if cache_key in _cache["data"] and _cache["timestamp"]:
        if datetime.now() - _cache["timestamp"] < CACHE_DURATION:
            return _cache["data"][cache_key]
    
    limit = min(limit, 100)
    articles = []
    
    # Try to fetch FRESH news from top headlines first
    try:
        if category and category != "general":
            params = {
                "apiKey": NEWS_API_KEY,
                "category": category,
                "pageSize": limit,
                "sortBy": "publishedAt"
            }
        else:
            params = {
                "apiKey": NEWS_API_KEY,
                "pageSize": limit,
                "sortBy": "publishedAt"
            }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        api_articles = response.json().get("articles", [])
        
        for a in api_articles:
            if a.get("title") and a.get("url"):
                articles.append({
                    "id": hash(a.get("url", "")) % ((2 ** 31) - 1),
                    "title": a.get("title", "No title"),
                    "description": a.get("description", ""),
                    "content": a.get("content", ""),
                    "url": a.get("url"),
                    "image": a.get("urlToImage"),
                    "source": a.get("source", {}).get("name", "Unknown"),
                    "source_id": a.get("source", {}).get("id", "unknown"),
                    "published_at": a.get("publishedAt", ""),
                    "category": category or "general",
                    "author": a.get("author", "Unknown"),
                    "is_reputable": True
                })
        
        _cache["timestamp"] = datetime.now()
        _cache["data"][cache_key] = articles
        
        print(f"✅ Fresh news loaded for category: {category or 'general'}")
        return articles[:limit]
    
    except Exception as e:
        print(f"⚠️ Could not fetch real news: {str(e)}")
        print(f"Trying fallback search...")
        
        # Fallback: try the everything endpoint with search
        try:
            query = category if category and category != "general" else "news"
            params = {
                "apiKey": NEWS_API_KEY,
                "q": query,
                "pageSize": limit,
                "sortBy": "publishedAt",
                "language": "en"
            }
            
            response = requests.get(EVERYTHING_URL, params=params, timeout=10)
            response.raise_for_status()
            
            api_articles = response.json().get("articles", [])
            
            for a in api_articles[:limit]:
                if a.get("title") and a.get("url"):
                    articles.append({
                        "id": hash(a.get("url", "")) % ((2 ** 31) - 1),
                        "title": a.get("title", "No title"),
                        "description": a.get("description", ""),
                        "content": a.get("content", ""),
                        "url": a.get("url"),
                        "image": a.get("urlToImage"),
                        "source": a.get("source", {}).get("name", "Unknown"),
                        "source_id": a.get("source", {}).get("id", "unknown"),
                        "published_at": a.get("publishedAt", ""),
                        "category": category or "general",
                        "author": a.get("author", "Unknown"),
                        "is_reputable": True
                    })
            
            _cache["timestamp"] = datetime.now()
            _cache["data"][cache_key] = articles
            
            print(f"✅ Using search results for: {category or 'general'}")
            return articles[:limit]
        
        except:
            print(f"❌ All news sources failed, using demo mode")
            return []

def search_news(query, limit=15, language="en"):
    if not query or len(query.strip()) < 2:
        raise Exception("Search query must be at least 2 characters long")
    
    limit = min(limit, 100)
    articles = []
    
    try:
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query,
            "pageSize": limit,
            "language": language,
            "sortBy": "publishedAt"
        }
        
        response = requests.get(EVERYTHING_URL, params=params, timeout=10)
        response.raise_for_status()
        
        api_articles = response.json().get("articles", [])
        
        for a in api_articles:
            if a.get("title") and a.get("url"):
                articles.append({
                    "id": hash(a.get("url", "")) % ((2 ** 31) - 1),
                    "title": a.get("title", "No title"),
                    "description": a.get("description", ""),
                    "content": a.get("content", ""),
                    "url": a.get("url"),
                    "image": a.get("urlToImage"),
                    "source": a.get("source", {}).get("name", "Unknown"),
                    "source_id": a.get("source", {}).get("id", "unknown"),
                    "published_at": a.get("publishedAt", ""),
                    "category": "search",
                    "author": a.get("author", "Unknown"),
                    "is_reputable": True
                })
        
        return articles[:limit]
    
    except:
        print(f"[Demo Mode] Using demo articles for search: {query}")
        return []