<div align="center">

# ⚡ AlgoMatch — Algorithmic Skill Optimizer

**Stop grinding blindly. Target your exact skill gaps.**

An intelligent, data-driven platform that analyzes any LeetCode profile, pinpoints algorithmic blind spots across 40+ topics, and recommends the highest-impact problems to solve next.

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

[🌐 Live Web Platform](https://problem-recommender.vercel.app) &nbsp;•&nbsp; [⚡ Streamlit Dashboard](http://localhost:8501) &nbsp;•&nbsp; [📖 Interactive API Docs](https://problem-recommender.vercel.app/docs)

</div>

---

## 🎯 Key Features

- **📊 Data-Driven Weakness Scoring**: Calculates a normalized weakness coefficient ($0.0 \rightarrow 1.0$) for 40+ algorithmic topics relative to your top strengths.
- **🎯 Precision Problem Ranking**: Ranks 3,900+ LeetCode problems in real time and surfaces the highest-value Easy, Medium, or Hard question targeting your gap.
- **📈 Creative 2-Graph Interactive Analytics**:
  - **📉 Top Topics Needing Practice**: Horizontal priority bar chart ranking your primary skill gaps.
  - **🍰 Solved Problems by Difficulty**: Clean donut chart visualizing your Easy, Medium, and Hard solve ratio.
- **⚡ Sub-Second Startup Caching**: Pre-fetches and caches 3,900+ problem catalog items at startup for instant sub-second recommendation responses.
- **🔄 Resilient GraphQL Pipeline**: Built with custom `User-Agent` headers and exponential backoff policies to bypass rate limits (HTTP 429).
- **🔒 Async Telemetry Logging**: Asynchronously logs user activity and stats to Supabase using FastAPI `BackgroundTasks`.

---

## 🏗️ System Architecture

```
problem-recommender-system/
├── backend/                  # Machine Learning & Backend API Layer
│   ├── api/
│   │   ├── main.py           # FastAPI Entrypoint & Web Route Orchestrator
│   │   ├── routes.py         # REST API Routes (/recommend, /stats, /update)
│   │   ├── tracker.py        # Supabase Activity Telemetry Interface
│   │   ├── schemas.py        # Pydantic Schemas & Data Contracts
│   │   ├── ui_html.py        # Single-Page Interactive Web Application Template
│   │   └── user_pipeline.py  # Scrape → Analyze → Rank ETL Orchestration
│   ├── scraper/
│   │   ├── fetch_profile.py  # Resilient LeetCode GraphQL Client
│   │   ├── parse_submissions.py # Raw Submission Parser & Tag Mapper
│   │   └── tag_analyzer.py   # Tag Weakness Matrix Calculations
│   ├── model/
│   │   ├── weakness_scorer.py# Algorithmic Weakness Scoring Engine
│   │   ├── problem_ranker.py # Catalog Ranking & Overlap Engine
│   │   └── model.pkl         # Trained Machine Learning Model Artifact
│   └── data/
│       └── problems_catalog.json # 3,900+ Pre-cached Catalog Problems
│
├── frontend/                 # Streamlit Web Application Layer
│   ├── dashboard.py          # Streamlit Organic Forest Green UI Entrypoint
│   └── ui/
│       ├── analytics.py      # 2-Graph Plotly Interactive Visualization
│       ├── client.py         # Cached API Client Interface
│       ├── components.py     # Header, Hero, Process Cards & Stat Cards
│       ├── recommendations.py# Target Recommendation Card & Detail Panel
│       └── styles.py         # Custom CSS Design System & Typography
│
├── tests/                    # Pytest Integration & Unit Test Suite
├── vercel.json               # Vercel Serverless Deployment Config
├── pyproject.toml            # Project Build & Vercel Entrypoint Spec
├── render.yaml               # Render Cloud Blueprint Specification
├── Dockerfile                # Docker Container Build Specification
└── requirements.txt          # Pinned Python Dependencies
```

### Request Execution Flow
```
User Enters LeetCode Username
             │
             ▼
FastAPI Request Handler (`/recommend?username=...`)
             │
     ┌───────┴───────┐
     │  Cache Hit?   │ ── Yes ──> Return Cached Recommendations (< 10ms)
     └───────┬───────┘
             │ No
             ▼
 1. Fetch Profile via LeetCode GraphQL API (Resilient Retries)
 2. Calculate Tag Weakness Coefficients (0.0 to 1.0)
 3. Rank 3,900+ Catalog Problems by Overlap
 4. Store Result in TTL Memory Cache (10 min)
 5. Dispatch Async Telemetry Logging Task (Supabase)
             │
             ▼
 Return Ranked Recommendations & Analytics JSON / UI
```

---

## 🧮 Mathematical Scoring Model

### 1. Tag Weakness Score
The system measures relative skill gap in a given topic using:

$$\text{Strength Score}_{\text{tag}} = \frac{\text{Solved Count}_{\text{tag}}}{\max(\text{Solved Counts across all tags})}$$

$$\text{Weakness Score}_{\text{tag}} = 1.0 - \text{Strength Score}_{\text{tag}}$$

* $\text{Weakness Score} = 0.0$ $\rightarrow$ Most practiced algorithmic domain.
* $\text{Weakness Score} = 1.0$ $\rightarrow$ Unpracticed algorithmic domain.

### 2. Problem Weakness Overlap
Unsolved catalog problems are scored by computing the mean weakness across all associated tags:

$$\text{Problem Score} = \frac{1}{n} \sum_{i=1}^{n} \text{Weakness Score}_{\text{tag}_i}$$

Problems are ranked in descending order of this score to surface the most impactful challenge.

---

## 📡 API Reference

All endpoints accept an optional query parameter `?username=<leetcode_username>`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Renders Single-Page Interactive Web Application |
| `GET` | `/recommend` | Top overall recommended problem |
| `GET` | `/recommend/easy` | Top Easy recommended problem |
| `GET` | `/recommend/medium` | Top Medium recommended problem |
| `GET` | `/recommend/hard` | Top Hard recommended problem |
| `GET` | `/stats` | User solved counts, percentages, and topic scores |
| `POST` | `/update` | Purges cache and forces fresh profile scrape |
| `POST` | `/admin/refresh-catalog` | Triggers background global problem catalog update (`X-Admin-Secret`) |
| `GET` | `/admin/users` | Fetches logged user telemetry (`X-Admin-Secret`) |

---

## 💻 Local Development Setup

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/Reena1912/problem-recommender.git
cd problem-recommender
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
LEETCODE_SESSION=your_session_cookie
LEETCODE_USERNAME=your_leetcode_username
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_key
ADMIN_SECRET=your_admin_secret
```

### 3. Launch Local Servers

**Backend API**:
```bash
python -m uvicorn backend.api.main:app --reload --port 8000
```

**Streamlit Dashboard**:
```bash
python -m streamlit run frontend/dashboard.py --server.port 8501
```

---

## 🚀 Deployment

### Vercel Serverless
1. Import repository on [Vercel](https://vercel.com/new).
2. Framework Preset: **Other**.
3. Deploy! Vercel automatically detects `pyproject.toml` and builds the serverless deployment.

### Render Cloud
1. Create a new **Blueprint** on [Render](https://dashboard.render.com).
2. Connect your repository — Render will automatically launch both `algomatch-api` and `algomatch-dashboard` using `render.yaml`.

---

<div align="center">
  <sub>Built with ⚡ · LeetCode GraphQL API · Machine Learning Weakness Ranking Engine</sub>
</div>
