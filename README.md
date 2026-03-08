# 📰 Student News Hub - Enhanced Edition

A modern, feature-rich news aggregation platform built for students who need to stay informed about global events, business developments, and industry trends. Perfect for accounting, finance, and business students!

## ✨ Features

### 🎯 Core Features
- **Global News Aggregation** - Fetch news from 50,000+ sources worldwide
- **Smart Categorization** - Organized by Business, Technology, Politics, Entertainment, Science, Sports, and Health
- **Intelligent Search** - Search across all news sources by keyword
- **Article Summarization** - Get quick AI-powered summaries of long articles
- **Save Favorites** - Bookmark important articles for later reading
- **Real-time Updates** - 30-minute cache ensures fresh content
- **Beautiful UI** - Modern, responsive dashboard that works on desktop and mobile

### 🚀 Technical Highlights
- **Flask Backend** - Lightweight Python web framework
- **RESTful API** - Clean, documented endpoints for all features
- **Smart Caching** - Reduces API calls and improves performance
- **Error Handling** - User-friendly error messages
- **Local Storage** - Favorites saved in browser (no account needed)
- **Responsive Design** - Works seamlessly on all devices

---

## 📋 Requirements

Before you begin, make sure you have:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **NewsAPI Key** (free at [newsapi.org](https://newsapi.org/)) - Get 100 free requests per day
- **Claude API Key** (optional, for AI summaries) - Get free credits at [Anthropic](https://console.anthropic.com)

---

## 🛠️ Installation

### Step 1: Clone/Extract the Project

```bash
# If you have the zip file, extract it
unzip student-news-app-enhanced.zip
cd student-news-app-enhanced
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# On Windows
echo. > .env

# On macOS/Linux
touch .env
```

Then open `.env` and add:

```
NEWS_API_KEY=your_newsapi_key_here
ANTHROPIC_API_KEY=your_claude_key_here  # Optional
```

#### Get Your API Keys:

**NewsAPI Key:**
1. Go to [https://newsapi.org/](https://newsapi.org/)
2. Click "Register" or "Get API Key"
3. Sign up with your email
4. Copy your API key
5. Paste it in `.env` file

**Claude API Key (Optional for summaries):**
1. Go to [https://console.anthropic.com](https://console.anthropic.com)
2. Sign up or login
3. Create an API key
4. Add credits (free trial available)
5. Copy your key and paste in `.env`

### Step 5: Run the Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

Open your browser and go to: **http://localhost:5000**

---

## 🎮 How to Use

### Main Dashboard

1. **Browse News** - Click category buttons to filter by topic
2. **Search** - Type keywords in the search bar to find specific news
3. **Save Favorites** - Click ⭐ to save articles you want to read later
4. **View Full Article** - Click → or anywhere on the card to read the full story
5. **Refresh** - Click 🔄 to get the latest news

### Categories Available

- 💼 **Business** - Markets, companies, financial news
- 💻 **Technology** - AI, software, startups, gadgets
- 🎬 **Entertainment** - Movies, music, celebrity news
- 🏛️ **Politics** - Government, elections, policy
- 🔬 **Science** - Research, discoveries, space
- ⚽ **Sports** - Games, teams, athletes
- 💊 **Health** - Medicine, wellness, fitness

---

## 🔧 API Endpoints

The app includes a powerful REST API. You can use these endpoints with tools like **curl**, **Postman**, or your own application:

### News Endpoints

**Get All News**
```bash
GET http://localhost:5000/api/news?limit=20&country=us
```

**Get News by Category**
```bash
GET http://localhost:5000/api/news/category/business
GET http://localhost:5000/api/news/category/technology
GET http://localhost:5000/api/news/category/entertainment
```

**Search News**
```bash
GET http://localhost:5000/api/news/search?q=accounting&limit=15
```

**Summarize Article**
```bash
POST http://localhost:5000/api/news/summarize
Content-Type: application/json

{
  "text": "Your article text here..."
}
```

### Configuration & Health

**Get App Configuration**
```bash
GET http://localhost:5000/api/config
```

**Health Check**
```bash
GET http://localhost:5000/api/health
```

---

## 📊 Project Structure

```
student-news-app-enhanced/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API keys)
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── services/
│   ├── __init__.py
│   ├── news_service.py      # NewsAPI integration
│   ├── summary_service.py   # AI summarization
│   └── categorizer_service.py # Smart categorization
└── templates/
    └── index.html           # Beautiful dashboard UI
```

---

## 🎓 Why This is Great for Students

### For Accounting & Finance Students:
- ✅ **Stay Updated on Markets** - Business category shows stock, earnings, and financial news
- ✅ **Track Regulations** - Politics section includes policy changes affecting finance
- ✅ **Company Research** - Search by company name to monitor their news
- ✅ **Economic Indicators** - Science category includes economic data and reports

### For All Students:
- ✅ **Quick Summaries** - Too busy? Get AI summaries of long articles
- ✅ **Save for Later** - Bookmark articles to read when you have time
- ✅ **Mobile Friendly** - Read news on your phone between classes
- ✅ **Always Free** - Uses free APIs with generous limits

---

## 🚀 Deployment

### Deploy to Heroku

1. **Install Heroku CLI** - [Download here](https://devcenter.heroku.com/articles/heroku-cli)

2. **Create Procfile**
```bash
echo "web: gunicorn app:app" > Procfile
pip install gunicorn
```

3. **Deploy**
```bash
heroku create your-app-name
heroku config:set NEWS_API_KEY=your_key
heroku config:set ANTHROPIC_API_KEY=your_key
git push heroku main
```

### Deploy to Other Platforms

- **Vercel**: [Vercel Flask Guide](https://vercel.com/guides/deploying-flask)
- **Render**: [Render Python Guide](https://render.com/docs/deploy-python)
- **Railway**: [Railway Python Guide](https://docs.railway.app/guides/python)
- **PythonAnywhere**: [PythonAnywhere Setup](https://www.pythonanywhere.com/)

---

## 🐛 Troubleshooting

### "NEWS_API_KEY not set" error
**Solution:** Add your API key to the `.env` file or set it as an environment variable

### "No articles found"
**Solution:** 
- Check your internet connection
- Verify your API key is valid at [newsapi.org](https://newsapi.org/)
- Try refreshing the page
- Check if you've exceeded API limits (100 requests/day free tier)

### Summaries not working
**Solution:**
- Claude API is optional - app works without it
- If you want summaries, get a free Claude API key from [console.anthropic.com](https://console.anthropic.com)
- Add it to your `.env` file and restart the app

### Port 5000 already in use
**Solution:** Use a different port
```bash
# Change port in app.py line 52 or use:
python app.py --port 8000
```

---

## 🔐 Security

- ✅ API keys are stored locally in `.env` (never commit this to git!)
- ✅ `.gitignore` prevents `.env` from being uploaded
- ✅ No user data is collected
- ✅ Favorites are stored only in your browser
- ✅ HTTPS recommended for production deployments

---

## 📈 Next Steps to Enhance

Want to extend this app? Here are ideas:

1. **Database Integration** - Store articles and user preferences in a database
2. **User Accounts** - Let students sync favorites across devices
3. **Email Alerts** - Send daily news digests to your inbox
4. **Advanced Analytics** - See what topics are trending
5. **Mobile App** - Convert to React Native or Flutter
6. **News Comparison** - See how different sources cover the same story
7. **Offline Mode** - Read saved articles without internet
8. **Dark Mode** - Add a dark theme option

---

## 📞 Support

If you encounter issues:

1. **Check the logs** - Look at the terminal output for error messages
2. **Verify API Keys** - Test your keys at their respective websites
3. **Check Requirements** - Run `pip list` to see installed packages
4. **Internet Connection** - Ensure you're connected to the internet
5. **Python Version** - Use Python 3.8 or higher

---

## 📄 License

This project is open source and available for educational use.

---

## 🎉 Enjoy!

You now have a professional news aggregation platform. Start exploring the world's events, bookmark important articles, and stay informed as a student!

**Pro Tips:**
- 📍 Set the browser tab as a bookmark for quick access
- 🔄 Refresh every morning for the latest news
- ⭐ Build a collection of important articles
- 🔍 Search for specific topics related to your studies

Happy news hunting! 📰
