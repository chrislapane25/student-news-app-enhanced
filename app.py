import sys
import traceback

try:
    from dotenv import load_dotenv
    load_dotenv()

    from flask import Flask, jsonify, render_template, request
    from services.news_service import get_news, search_news
    from services.research_service import search_research, get_research_by_field
    from services.summary_service import summarize_article
    import os
    from datetime import datetime

    app = Flask(__name__)

    # Configuration
    app.config['JSON_SORT_KEYS'] = False
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/api/news")
    def api_news_all():
        """Get all news articles with optional filtering"""
        try:
            limit = request.args.get('limit', 20, type=int)
            
            if limit > 100:
                limit = 100
                
            news_items = get_news(category=None, limit=limit)
            
            return jsonify({
                "status": "success",
                "count": len(news_items),
                "timestamp": datetime.now().isoformat(),
                "news": news_items
            })
        except Exception as e:
            print(f"ERROR in api_news_all: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    @app.route("/api/news/category/<category>")
    def api_news_by_category(category):
        """Get news by category"""
        try:
            limit = request.args.get('limit', 15, type=int)
            
            valid_categories = ['business', 'entertainment', 'general', 'health', 
                               'science', 'sports', 'technology', 'politics']
            
            if category.lower() not in valid_categories:
                return jsonify({
                    "status": "error",
                    "message": f"Invalid category. Valid categories: {', '.join(valid_categories)}"
                }), 400
                
            news_items = get_news(category=category.lower(), limit=limit)
            
            return jsonify({
                "status": "success",
                "category": category,
                "count": len(news_items),
                "timestamp": datetime.now().isoformat(),
                "news": news_items
            })
        except Exception as e:
            print(f"ERROR in api_news_by_category: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    @app.route("/api/news/search")
    def api_search_news():
        """Search news by keyword"""
        try:
            query = request.args.get('q', '', type=str)
            limit = request.args.get('limit', 15, type=int)
            
            if not query:
                return jsonify({
                    "status": "error",
                    "message": "Please provide a search query (q parameter)"
                }), 400
                
            news_items = search_news(query=query, limit=limit)
            
            return jsonify({
                "status": "success",
                "query": query,
                "count": len(news_items),
                "timestamp": datetime.now().isoformat(),
                "news": news_items
            })
        except Exception as e:
            print(f"ERROR in api_search_news: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    @app.route("/api/news/summarize", methods=['POST'])
    def api_summarize():
        """Get a summary of an article"""
        try:
            data = request.get_json()
            
            if not data or 'text' not in data:
                return jsonify({
                    "status": "error",
                    "message": "Please provide article text in JSON body: {\"text\": \"...\"}"
                }), 400
                
            text = data['text']
            
            if len(text) < 50:
                return jsonify({
                    "status": "error",
                    "message": "Article text too short to summarize (minimum 50 characters)"
                }), 400
                
            summary = summarize_article(text)
            
            return jsonify({
                "status": "success",
                "original_length": len(text),
                "summary": summary,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"ERROR in api_summarize: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    # ===== RESEARCH ENDPOINTS =====

    @app.route("/api/research/search")
    def api_search_research():
        """Search for research papers"""
        try:
            query = request.args.get('q', '', type=str)
            limit = request.args.get('limit', 15, type=int)
            
            if not query:
                return jsonify({
                    "status": "error",
                    "message": "Please provide a search query (q parameter)"
                }), 400
            
            papers = search_research(query=query, limit=limit)
            
            return jsonify({
                "status": "success",
                "query": query,
                "count": len(papers),
                "timestamp": datetime.now().isoformat(),
                "papers": papers
            })
        except Exception as e:
            print(f"ERROR in api_search_research: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    @app.route("/api/research/field/<field>")
    def api_research_by_field(field):
        """Get research by field"""
        try:
            limit = request.args.get('limit', 15, type=int)
            
            valid_fields = ['medicine', 'biology', 'microbiology', 'health', 'physics', 'chemistry']
            
            if field.lower() not in valid_fields:
                return jsonify({
                    "status": "error",
                    "message": f"Invalid field. Valid fields: {', '.join(valid_fields)}"
                }), 400
            
            papers = get_research_by_field(field=field, limit=limit)
            
            return jsonify({
                "status": "success",
                "field": field,
                "count": len(papers),
                "timestamp": datetime.now().isoformat(),
                "papers": papers
            })
        except Exception as e:
            print(f"ERROR in api_research_by_field: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    @app.route("/api/config")
    def api_config():
        """Get app configuration"""
        return jsonify({
            "status": "success",
            "app": "Student Knowledge Hub",
            "version": "2.0.0",
            "features": [
                "Global news aggregation",
                "Research paper search",
                "Category filtering",
                "Search functionality",
                "Article summarization",
                "Reputable sources only"
            ],
            "news_categories": ['business', 'entertainment', 'general', 'health', 
                          'science', 'sports', 'technology', 'politics'],
            "research_fields": ['medicine', 'biology', 'microbiology', 'health', 'physics', 'chemistry'],
            "api_key_configured": bool(NEWS_API_KEY)
        })

    @app.route("/api/health")
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "service": "student-knowledge-app",
            "timestamp": datetime.now().isoformat()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Endpoint not found. Check /api/config for available endpoints."
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    if __name__ == "__main__":
        print("\n" + "="*60)
        print("✅ Student Knowledge Hub - Starting Up")
        print("="*60)
        print(f"✅ NEWS_API_KEY is set: {bool(NEWS_API_KEY)}")
        if NEWS_API_KEY:
            print(f"   API Key length: {len(NEWS_API_KEY)} characters")
        print("="*60 + "\n")
        
        if not NEWS_API_KEY:
            print("\n⚠️  WARNING: NEWS_API_KEY environment variable is not set!")
            print("Get a free API key from https://newsapi.org/")
            print("Add it to your .env file\n")
        
        app.run(debug=True, host="0.0.0.0", port=5000)

except Exception as e:
    print("\n" + "="*60)
    print("❌ STARTUP ERROR")
    print("="*60)
    print(f"Error: {str(e)}")
    print("="*60)
    print("\nFull traceback:")
    traceback.print_exc()
    print("="*60 + "\n")
    sys.exit(1)