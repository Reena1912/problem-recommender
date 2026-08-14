<div align="center">

#  LeetCode Recommender 

**Stop grinding blindly. Target your exact skill gaps.**

An intelligent, production-ready system that analyzes any LeetCode profile, identifies algorithmic blind spots, and recommends the most impactful problems to solve next — backed by data-driven weakness scoring.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**[ Live Dashboard](https://problem-recommender-dashboard.streamlit.app/)** &nbsp;|&nbsp; **[ Interactive API Docs](https://leetcode-recommender-api.onrender.com/docs)**

</div>

---

##  Key Features

* **Data-Driven Weakness Scoring**: Calculates a weakness coefficient for every algorithmic tag (0.0 to 1.0) based on your solved ratio relative to your strengths.
* **Instant Recommendations**: Ranks 3,900+ LeetCode problems and serves the top Easy, Medium, or Hard problem targeting your specific gap.
* **Visual Analytics**: Interactive radar charts, weakness bars, and pie charts powered by Plotly.
* **Startup Catalog Caching**: Pre-fetches and caches the global LeetCode problem catalog at startup to achieve sub-second backend load times.
* **Asynchronous Database Logging**: Logs user activity and stats to Supabase using FastAPI `BackgroundTasks` to prevent database latency from blocking the frontend.
* **Resilient Scraping**: Scrapers are protected with custom `User-Agent` headers and exponential backoff retry policies to bypass LeetCode's rate-limiting (HTTP 429).
* **Secure Admin Operations**: Admin endpoints for catalog refreshes and user auditing are locked behind secure `X-Admin-Secret` headers.

---

##  System Architecture

```
##  System Architecture

```
problem-recommender-system/
├── backend/                  # Backend Service & Machine Learning Layer
│   ├── api/
│   │   ├── main.py           # FastAPI Entry Point (loads 3,900+ problems catalog at startup)
│   │   ├── routes.py         # HTTP Endpoints (/recommend, /stats, /subscribe, /update)
│   │   ├── newsletter.py     # Newsletter subscription handler & SMTP dispatcher
│   │   ├── tracker.py        # Database interface logging user activity to Supabase
│   │   ├── schemas.py        # Pydantic validation & response models
│   │   └── user_pipeline.py  # ETL Orchestration + 10-minute local TTL caching
│   ├── scraper/
│   │   ├── fetch_profile.py  # LeetCode GraphQL Client (with retry backoff)
│   │   ├── parse_submissions.py # Raw JSON parser and tag mapper
│   │   └── tag_analyzer.py   # Core weakness calculation calculations
│   ├── model/
│   │   ├── weakness_scorer.py# Ranks problems based on tag scores
│   │   ├── problem_ranker.py # Ranks unsolved problems
│   │   └── model.pkl         # Machine learning model artifact
│   ├── data/
│   │   ├── problems_catalog.json # Cached global problems catalog (3,900+ problems)
│   │   ├── subscribers.json  # Saved email subscribers dataset
│   │   └── database_schema.sql # Supabase SQL schema
│   └── config.py             # Environment configurations loader
│
├── frontend/                 # Frontend Web Application Layer
│   ├── dashboard.py          # Streamlit organic sage & forest green UI application
│   └── ui/
│       ├── analytics.py      # Plotly interactive charts & data visualization
│       ├── client.py         # Fast sub-second @st.cache_data API client
│       ├── components.py     # Nav bar, hero section, process cards & stat cards
│       ├── recommendations.py# Recommendation problem cards & detail panels
│       └── styles.py         # Custom typography & design system stylesheet
│
├── tests/                    # Pytest Integration & Unit Test Suite
├── Dockerfile                # Container deployment build spec
├── docker-compose.yml        # Docker composition setup
├── render.yaml               # Render cloud deployment specification
├── requirements.txt          # Pinned Python dependencies
└── .env                      # Local environment secrets
```

### Request Flow Diagram
```
User types LeetCode username on Streamlit Web App
                       ↓
         Streamlit sends HTTP Request
         GET /recommend?username=username
                       ↓
        FastAPI checks local TTL Cache
        ├── Hit?  → Return cached JSON instantly (< 10ms)
        └── Miss? 
             ├── Fetch profile from LeetCode GraphQL API
             │   (Resilient retries / User-Agent headers)
             ├── Compute tag weakness scores (0.0 - 1.0)
             ├── Rank 3,900+ problems by weakness overlap
             ├── Cache result for 10 minutes in memory
             ├── Start async background logging task (Supabase)
             ↓
         Return recommendations response
```

---

##  Mathematical Model

### 1. Tag Weakness Scoring
The system measures a user's relative weakness in a particular topic (tag) using this formula:

$$\text{Strength Score}_{\text{tag}} = \frac{\text{Solved Count}_{\text{tag}}}{\max(\text{Solved Counts across all tags})}$$

$$\text{Weakness Score}_{\text{tag}} = 1 - \text{Strength Score}_{\text{tag}}$$

* *A weakness score of `0.0` represents your most practiced topic.*
* *A weakness score of `1.0` represents a topic you have never solved.*

### 2. Problem Weakness Score
To score an unsolved problem, the system averages the weakness scores of all the tags associated with that problem:

$$\text{Problem Score} = \frac{\sum_{i=1}^{n} \text{Weakness Score}_{\text{tag}_i}}{n}$$

All unsolved problems are ranked in descending order of this score. The top results target your absolute largest skill gaps.

---

##  API Reference

All routes accept `?username=<leetcode_username>`. If omitted, they fall back to the default `LEETCODE_USERNAME` in `.env`.

| Method | Endpoint | Headers | Description |
|--------|----------|---------|-------------|
| `GET` | `/` | None | API metadata and usage stats |
| `GET` | `/recommend` | None | Top recommendation (any difficulty) |
| `GET` | `/recommend/easy` | None | Top Easy recommendation |
| `GET` | `/recommend/medium` | None | Top Medium recommendation |
| `GET` | `/recommend/hard` | None | Top Hard recommendation |
| `GET` | `/stats` | None | User solved counts, totals, and tag scores |
| `POST` | `/subscribe` | None | Registers email newsletter subscription |
| `POST` | `/update` | None | Purges cache and forces profile re-scrape |
| `POST` | `/admin/refresh-catalog` | `X-Admin-Secret` | Triggers background global problem catalog refresh |
| `GET` | `/admin/users` | `X-Admin-Secret` | Returns logged statistics for all users |

---

##  Running Locally

### Prerequisites
* Python 3.11+
* A LeetCode account & session cookie

### 1. Setup Virtual Environment
```bash
git clone https://github.com/Reena1912/leetcode-recommender.git
cd leetcode-recommender
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Credentials
1. Log into [leetcode.com](https://leetcode.com).
2. Open Browser DevTools (`F12` or `Ctrl+Shift+I`) -> **Application** -> **Cookies** -> `https://leetcode.com`.
3. Copy the value of the **`LEETCODE_SESSION`** cookie.
4. Create a `.env` file in the project root:
   ```env
   LEETCODE_SESSION=your_leetcode_session_cookie
   LEETCODE_USERNAME=your_leetcode_username
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_SERVICE_KEY=your_supabase_anon_key
   ADMIN_SECRET=your_admin_secret_string
   ```

### 3. Run the Services
**Terminal 1 (Backend API)**:
```bash
python -m uvicorn backend.api.main:app --reload
```
*(On the first run, the API will take ~30 seconds to download and cache the global 3,900+ problem catalog from LeetCode).*

**Terminal 2 (Streamlit Frontend Dashboard)**:
```bash
python -m streamlit run frontend/dashboard.py
```



---

<div align="center">
  <sub>Built with ⚡ · LeetCode GraphQL API · Weakness-Score Ranking · Production Optimized</sub>
</div>
