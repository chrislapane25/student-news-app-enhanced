import os
import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
EVERYTHING_URL = "https://newsapi.org/v2/everything"

CACHE_DURATION = timedelta(minutes=30)
_cache = {"timestamp": None, "data": {}}

# South African News RSS Feeds (Verified Working)
SA_RSS_FEEDS = {
    "Mail & Guardian": "https://mg.co.za/feed",
    "Daily Maverick": "https://www.dailymaverick.co.za/dmrss",
    "IOL News": "https://rss.iol.io/iol/news",
    "The South African": "https://thesouthafrican.com/feed",
    "TechCentral": "https://techcentral.co.za/feed",
    "MyBroadband": "https://mybroadband.co.za/news/feed",
    "Moneyweb": "https://www.moneyweb.co.za/feed/",
    "BusinessTech": "https://businesstech.co.za/news/feed/",
}

def parse_rss_feed(feed_url, source_name):
    """Parse RSS feed and return articles"""
    articles = []
    try:
        response = requests.get(feed_url, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        # Handle different RSS namespaces
        ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}
        
        for item in root.findall('.//item')[:10]:  # Get first 10 items
            title_elem = item.find('title')
            link_elem = item.find('link')
            desc_elem = item.find('description')
            pub_date_elem = item.find('pubDate')
            
            if title_elem is not None and link_elem is not None:
                title = title_elem.text or "No title"
                link = link_elem.text or ""
                description = desc_elem.text if desc_elem is not None else ""
                pub_date = pub_date_elem.text if pub_date_elem is not None else ""
                
                # Clean description
                if description:
                    description = description.replace('<![CDATA[', '').replace(']]>', '')
                    description = description[:200]  # Limit length
                
                articles.append({
                    "id": hash(link) % ((2 ** 31) - 1),
                    "title": title[:150],
                    "description": description,
                    "content": description,
                    "url": link,
                    "image": None,
                    "source": f"{source_name} (SA)",
                    "source_id": source_name.lower().replace(" ", "-"),
                    "published_at": pub_date,
                    "category": "general",
                    "author": source_name,
                    "is_reputable": True,
                    "is_sa": True
                })
    except Exception as e:
        print(f"⚠️ Error parsing RSS feed ({source_name}): {str(e)}")
    
    return articles

def get_sa_news(limit=10):
    """Get news from South African RSS feeds"""
    all_articles = []
    
    print("[SA News] Fetching from RSS feeds...")
    
    for source_name, feed_url in SA_RSS_FEEDS.items():
        articles = parse_rss_feed(feed_url, source_name)
        all_articles.extend(articles)
    
    # Sort by date (newest first)
    all_articles = sorted(all_articles, 
                         key=lambda x: x.get('published_at', ''), 
                         reverse=True)
    
    print(f"✅ Got {len(all_articles)} SA articles from RSS feeds")
    return all_articles[:limit]

def get_news(category=None, country="us", limit=10, language="en"):
    global _cache
    
    cache_key = f"{category or 'general'}_fresh"
    
    # Return cached data if available
    if cache_key in _cache["data"] and _cache["timestamp"]:
        if datetime.now() - _cache["timestamp"] < CACHE_DURATION:
            return _cache["data"][cache_key]
    
    limit = min(limit, 100)
    articles = []
    
    # PRIORITY: Get SA news first (50% of results)
    try:
        sa_articles = get_sa_news(limit=limit // 2)
        articles.extend(sa_articles)
        print(f"[SA News] Added {len(sa_articles)} SA articles")
    except Exception as e:
        print(f"⚠️ SA news failed: {str(e)}")
    
    # FALLBACK: Get global news (other 50%)
    try:
        query = category if category and category != "general" else "news"
        
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query,
            "pageSize": limit - len(articles),  # Fill remaining slots
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
                    "category": category or "general",
                    "author": a.get("author", "Unknown"),
                    "is_reputable": True,
                    "is_sa": False
                })
        
        print(f"[Global News] Added {len(api_articles)} global articles")
    
    except Exception as e:
        print(f"⚠️ Global news failed: {str(e)}")
    
    # Cache results
    _cache["timestamp"] = datetime.now()
    _cache["data"][cache_key] = articles[:limit]
    
    print(f"✅ Total articles: {len(articles[:limit])}")
    return articles[:limit]

def search_news(query, limit=15, language="en"):
    if not query or len(query.strip()) < 2:
        raise Exception("Search query must be at least 2 characters long")
    
    limit = min(limit, 100)
    articles = []
    
    try:
        # Try SA search first
        sa_articles = get_sa_news(limit=limit // 2)
        
        # Filter SA articles by query
        filtered_sa = [a for a in sa_articles 
                      if query.lower() in a['title'].lower() 
                      or query.lower() in a['description'].lower()]
        
        articles.extend(filtered_sa)
        print(f"[SA Search] Found {len(filtered_sa)} SA results for: {query}")
    except Exception as e:
        print(f"⚠️ SA search failed: {str(e)}")
    
    try:
        # Get global search results
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query,
            "pageSize": limit - len(articles),
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
                    "is_reputable": True,
                    "is_sa": False
                })
        
        print(f"[Global Search] Found {len(api_articles)} global results for: {query}")
    
    except Exception as e:
        print(f"⚠️ Global search failed: {str(e)}")
    
    return articles[:limit]