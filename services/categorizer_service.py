"""
Smart categorization service for news articles.
Helps organize articles into meaningful categories based on content.
"""

CATEGORY_KEYWORDS = {
    'business': [
        'business', 'market', 'stock', 'finance', 'earnings', 'revenue', 'profit',
        'corporate', 'company', 'trade', 'economy', 'economic', 'investment',
        'financial', 'banking', 'bank', 'loan', 'debt', 'merger', 'acquisition',
        'ipo', 'startup', 'venture', 'ceo', 'executive', 'cryptocurrency', 'crypto'
    ],
    'politics': [
        'politics', 'political', 'government', 'congress', 'senate', 'parliament',
        'election', 'vote', 'campaign', 'president', 'minister', 'minister', 'law',
        'legislation', 'bill', 'policy', 'democrat', 'republican', 'party', 'trump',
        'biden', 'parliament', 'diplomatic', 'international relation'
    ],
    'entertainment': [
        'entertainment', 'movie', 'film', 'actor', 'actress', 'celebrity', 'music',
        'musician', 'concert', 'album', 'song', 'television', 'tv', 'show', 'series',
        'hollywood', 'award', 'oscars', 'grammy', 'golden globe', 'netflix', 'streaming',
        'broadway', 'theater', 'comedian', 'comedy', 'drama', 'romance'
    ],
    'technology': [
        'technology', 'tech', 'software', 'hardware', 'computer', 'mobile', 'app',
        'artificial intelligence', 'ai', 'machine learning', 'data', 'cyber',
        'security', 'hacking', 'privacy', 'internet', 'web', 'digital', 'online',
        'startup', 'google', 'apple', 'microsoft', 'amazon', 'meta', 'facebook',
        'robot', 'automation', 'blockchain', 'metaverse', 'vr', 'ar'
    ],
    'science': [
        'science', 'scientific', 'research', 'study', 'scientist', 'biology',
        'chemistry', 'physics', 'space', 'nasa', 'astronomy', 'universe',
        'climate', 'environment', 'medical', 'medicine', 'doctor', 'hospital',
        'vaccine', 'disease', 'health', 'pandemic', 'discovery', 'breakthrough'
    ],
    'sports': [
        'sports', 'sport', 'game', 'team', 'player', 'coach', 'football',
        'basketball', 'baseball', 'soccer', 'hockey', 'tennis', 'golf',
        'nfl', 'nba', 'nhl', 'mlb', 'nfl', 'world cup', 'olympics',
        'champion', 'championship', 'league', 'tournament', 'match', 'score'
    ],
    'health': [
        'health', 'healthcare', 'medical', 'medicine', 'doctor', 'hospital',
        'patient', 'disease', 'illness', 'treatment', 'therapy', 'vaccine',
        'virus', 'bacteria', 'pandemic', 'epidemic', 'covid', 'fitness',
        'wellness', 'nutrition', 'diet', 'exercise', 'mental health', 'psychology'
    ]
}

def categorize_article(title, description, content=""):
    """
    Categorize an article based on its content.
    
    Args:
        title: Article title
        description: Article description
        content: Article content (optional)
    
    Returns:
        Tuple of (primary_category, confidence_score)
    """
    text = f"{title} {description} {content}".lower()
    
    scores = {}
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                # Weight title matches higher
                if keyword in title.lower():
                    score += 3
                # Weight description matches medium
                elif keyword in description.lower():
                    score += 2
                # Weight content matches lower
                else:
                    score += 1
        
        scores[category] = score
    
    # Get highest scoring category
    if max(scores.values()) > 0:
        primary_category = max(scores, key=scores.get)
        confidence = min(scores[primary_category] / 10, 1.0)  # Normalize to 0-1
        return primary_category, confidence
    
    return 'general', 0.0

def enhance_articles_with_categories(articles):
    """
    Add smart categorization to articles.
    
    Args:
        articles: List of article dictionaries
    
    Returns:
        Articles with enhanced category information
    """
    for article in articles:
        category, confidence = categorize_article(
            article.get('title', ''),
            article.get('description', ''),
            article.get('content', '')
        )
        article['smart_category'] = category
        article['category_confidence'] = round(confidence, 2)
    
    return articles
