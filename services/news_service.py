import os
import requests
from datetime import datetime, timedelta

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

CACHE_DURATION = timedelta(minutes=30)
_cache = {"timestamp": None, "data": {}}

# Demo articles for when API is unavailable
DEMO_ARTICLES = {
    "general": [
        {
            "id": 1,
            "title": "Global Markets React to Economic Data",
            "description": "World markets move on latest economic indicators",
            "content": "Global financial markets showed mixed reactions today...",
            "url": "https://www.bbc.com/news",
            "image": "https://via.placeholder.com/400x300?text=BBC+News",
            "source": "BBC News (UK)",
            "source_id": "bbc-news",
            "published_at": datetime.now().isoformat(),
            "category": "general",
            "author": "BBC News",
            "is_reputable": True
        },
        {
            "id": 2,
            "title": "Technology Leaders Announce New Partnerships",
            "description": "Major tech companies join forces on new initiative",
            "content": "In a surprising move, several technology companies...",
            "url": "https://www.cnn.com",
            "image": "https://via.placeholder.com/400x300?text=CNN",
            "source": "CNN (USA)",
            "source_id": "cnn",
            "published_at": datetime.now().isoformat(),
            "category": "general",
            "author": "CNN",
            "is_reputable": True
        },
        {
            "id": 3,
            "title": "Business Leaders Meet at International Summit",
            "description": "Global business conference discusses future strategies",
            "content": "Top executives from around the world gathered...",
            "url": "https://www.reuters.com",
            "image": "https://via.placeholder.com/400x300?text=Reuters",
            "source": "Reuters (International)",
            "source_id": "reuters",
            "published_at": datetime.now().isoformat(),
            "category": "general",
            "author": "Reuters",
            "is_reputable": True
        }
    ],
    "business": [
        {
            "id": 4,
            "title": "Stock Markets Close Higher",
            "description": "Major indices finish day in positive territory",
            "content": "Financial markets ended the day with gains across...",
            "url": "https://www.bloomberg.com",
            "image": "https://via.placeholder.com/400x300?text=Bloomberg",
            "source": "Bloomberg (USA)",
            "source_id": "bloomberg",
            "published_at": datetime.now().isoformat(),
            "category": "business",
            "author": "Bloomberg",
            "is_reputable": True
        },
        {
            "id": 5,
            "title": "Corporate Earnings Beat Expectations",
            "description": "Major corporation reports strong quarterly results",
            "content": "A leading company announced earnings that...",
            "url": "https://www.cnbc.com",
            "image": "https://via.placeholder.com/400x300?text=CNBC",
            "source": "CNBC (USA)",
            "source_id": "cnbc",
            "published_at": datetime.now().isoformat(),
            "category": "business",
            "author": "CNBC",
            "is_reputable": True
        }
    ],
    "technology": [
        {
            "id": 6,
            "title": "New AI Breakthrough Announced",
            "description": "Researchers achieve milestone in artificial intelligence",
            "content": "Scientists unveiled a major breakthrough in AI...",
            "url": "https://www.techcrunch.com",
            "image": "https://via.placeholder.com/400x300?text=TechCrunch",
            "source": "TechCrunch (USA)",
            "source_id": "techcrunch",
            "published_at": datetime.now().isoformat(),
            "category": "technology",
            "author": "TechCrunch",
            "is_reputable": True
        }
    ]
}

def get_news(category=None, country="us", limit=10, language="en"):
    global _cache
    
    cache_key = f"{category or 'general'}_reputable"
    
    # Return cached data if available
    if cache_key in _cache["data"] and _cache["timestamp"]:
        if datetime.now() - _cache["timestamp"] < CACHE_DURATION:
            return _cache["data"][cache_key]
    
    limit = min(limit, 100)
    query = category if category and category != "general" else "general"
    
    articles = []
    
    # Try to fetch from API
    try:
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query,
            "pageSize": limit,
            "language": language,
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
                    "category": query,
                    "author": a.get("author", "Unknown"),
                    "is_reputable": True
                })
        
        _cache["timestamp"] = datetime.now()
        _cache["data"][cache_key] = articles
        
        return articles[:limit]
    
    except:
        # If API fails, use demo data
        print(f"[Demo Mode] Using demo articles for category: {query}")
        
        demo_key = query if query in DEMO_ARTICLES else "general"
        demo_articles = DEMO_ARTICLES.get(demo_key, DEMO_ARTICLES["general"])
        
        _cache["timestamp"] = datetime.now()
        _cache["data"][cache_key] = demo_articles
        
        return demo_articles[:limit]

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
                    "category": "search",
                    "author": a.get("author", "Unknown"),
                    "is_reputable": True
                })
        
        return articles[:limit]
    
    except:
        print(f"[Demo Mode] Using demo articles for search: {query}")
        # Return relevant demo articles
        return DEMO_ARTICLES["general"][:limit]