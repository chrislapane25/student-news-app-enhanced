import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from urllib.parse import quote

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ARXIV_BASE = "http://export.arxiv.org/api/query"
# Google Scholar alternative: using free APIs only

CACHE_DURATION = timedelta(minutes=30)
_cache = {"timestamp": None, "data": {}}

# arXiv categories (excluding CS)
ARXIV_CATEGORIES = {
    "physics": "Physics (all areas)",
    "math": "Mathematics",
    "astro-ph": "Astrophysics",
    "cond-mat": "Condensed Matter",
    "bio": "Quantitative Biology",
    "q-bio": "Quantitative Biology",
}

def search_pubmed(query, limit=10):
    """Search PubMed for medical/biology research papers"""
    articles = []
    
    print(f"[PubMed] Searching for: {query}")
    
    try:
        # Step 1: Search for paper IDs
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": limit,
            "rettype": "json",
            "sort": "date"
        }
        
        search_response = requests.get(
            f"{PUBMED_BASE}/esearch.fcgi",
            params=search_params,
            timeout=10
        )
        search_response.raise_for_status()
        search_data = search_response.json()
        
        ids = search_data.get("esearchresult", {}).get("idlist", [])
        
        if not ids:
            print(f"[PubMed] No results found for: {query}")
            return articles
        
        # Step 2: Fetch details for each paper
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "rettype": "json",
            "retmode": "json"
        }
        
        fetch_response = requests.get(
            f"{PUBMED_BASE}/efetch.fcgi",
            params=fetch_params,
            timeout=10
        )
        fetch_response.raise_for_status()
        fetch_data = fetch_response.json()
        
        papers = fetch_data.get("result", {}).get("uids", [])
        
        for paper_id in papers:
            if paper_id == "uids":
                continue
            
            paper_data = fetch_data.get("result", {}).get(paper_id, {})
            
            title = paper_data.get("title", "No title")
            abstract = paper_data.get("abstract", "No abstract available")
            pub_date = paper_data.get("pubdate", "")
            authors = paper_data.get("authors", [])
            
            # Format authors
            author_names = []
            for author in authors[:3]:
                author_names.append(author.get("name", "Unknown"))
            author_str = ", ".join(author_names) if author_names else "Unknown"
            
            articles.append({
                "id": hash(paper_id) % ((2 ** 31) - 1),
                "title": title[:200],
                "description": abstract[:300],
                "abstract": abstract,
                "content": abstract,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{paper_id}/",
                "image": None,
                "source": "PubMed",
                "source_id": "pubmed",
                "published_at": pub_date,
                "category": "research",
                "author": author_str,
                "is_reputable": True,
                "paper_id": paper_id,
                "paper_type": "journal"
            })
        
        print(f"[PubMed] Found {len(articles)} papers for: {query}")
        return articles
    
    except Exception as e:
        print(f"⚠️ PubMed search failed: {str(e)[:50]}")
        return articles

def search_arxiv(query, limit=15, category=None):
    """Search arXiv for physics, math, biology, chemistry research"""
    articles = []
    
    print(f"[arXiv] Searching for: {query}")
    
    try:
        # Build query
        search_query = f"search_query=all:{query}"
        
        # Add category filter if specified
        if category and category in ARXIV_CATEGORIES:
            search_query += f"+AND+cat:{category}"
        
        # Query parameters
        params = f"{search_query}&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending"
        
        response = requests.get(
            f"{ARXIV_BASE}?{params}",
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        # Define namespace
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', ns):
            title_elem = entry.find('atom:title', ns)
            summary_elem = entry.find('atom:summary', ns)
            published_elem = entry.find('atom:published', ns)
            author_elem = entry.find('atom:author', ns)
            id_elem = entry.find('atom:id', ns)
            
            title = title_elem.text if title_elem is not None else "No title"
            summary = summary_elem.text if summary_elem is not None else "No abstract"
            published = published_elem.text if published_elem is not None else ""
            author = author_elem.find('atom:name', ns).text if author_elem is not None else "Unknown"
            arxiv_id = id_elem.text if id_elem is not None else ""
            
            # Clean up summary
            if summary:
                summary = summary.replace('\n', ' ').strip()
            
            # Extract arXiv ID
            if arxiv_id:
                arxiv_id = arxiv_id.split('/abs/')[-1]
                url = f"https://arxiv.org/abs/{arxiv_id}"
            else:
                url = ""
            
            if url:
                articles.append({
                    "id": hash(arxiv_id) % ((2 ** 31) - 1),
                    "title": title[:200],
                    "description": summary[:300],
                    "abstract": summary,
                    "content": summary,
                    "url": url,
                    "image": None,
                    "source": "arXiv",
                    "source_id": "arxiv",
                    "published_at": published,
                    "category": "research",
                    "author": author,
                    "is_reputable": True,
                    "paper_id": arxiv_id,
                    "paper_type": "preprint"
                })
        
        print(f"[arXiv] Found {len(articles)} papers for: {query}")
        return articles
    
    except Exception as e:
        print(f"⚠️ arXiv search failed: {str(e)[:50]}")
        return articles

def search_research(query, limit=30, source="all"):
    """Search across reliable research sources"""
    if not query or len(query.strip()) < 2:
        raise Exception("Search query must be at least 2 characters long")
    
    limit = min(limit, 100)
    all_papers = []
    
    print(f"\n🔬 RESEARCH SEARCH for: {query}")
    
    # Search arXiv (Physics, Math, Biology, Chemistry - very reliable)
    if source in ["all", "arxiv"]:
        try:
            papers = search_arxiv(query, limit=limit//2)
            all_papers.extend(papers)
        except Exception as e:
            print(f"⚠️ arXiv error: {str(e)[:30]}")
    
    # Search PubMed (Medical/Health - reliable)
    if source in ["all", "pubmed"]:
        try:
            papers = search_pubmed(query, limit=limit//2)
            all_papers.extend(papers)
        except Exception as e:
            print(f"⚠️ PubMed error: {str(e)[:30]}")
    
    # Remove duplicates by title
    seen_titles = set()
    unique_papers = []
    for paper in all_papers:
        title_lower = paper['title'].lower()
        if title_lower not in seen_titles:
            unique_papers.append(paper)
            seen_titles.add(title_lower)
    
    # Sort by date (newest first)
    unique_papers = sorted(unique_papers,
                          key=lambda x: x.get('published_at', '') or '',
                          reverse=True)
    
    print(f"✅ Total research results: {len(unique_papers[:limit])}\n")
    return unique_papers[:limit]

def get_research_by_field(field, limit=15):
    """Get research papers by field"""
    field_queries = {
        "medicine": "medicine disease treatment clinical",
        "biology": "biology organism cell genetics",
        "microbiology": "microbiology bacteria virus microorganism",
        "health": "health healthcare medical patient",
        "physics": "physics quantum mechanics particle",
        "chemistry": "chemistry chemical reaction molecular",
    }
    
    query = field_queries.get(field.lower(), field)
    return search_research(query, limit=limit)