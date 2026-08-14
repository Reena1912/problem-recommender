<div align="center">

# AlgoMatch — Algorithmic Skill Optimizer

**Stop grinding blindly. Target your exact skill gaps.**

An intelligent, data-driven platform that analyzes any LeetCode profile, pinpoints algorithmic blind spots across 40+ topics, and recommends the highest-impact problems to solve next.

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

[Live Web Platform](https://problem-recommender.vercel.app) &nbsp;•&nbsp; [Streamlit Dashboard](http://localhost:8501) &nbsp;•&nbsp; [Interactive API Docs](https://problem-recommender.vercel.app/docs)

</div>

---

## About The Platform

AlgoMatch is an intelligent algorithmic skill optimization engine designed for software engineers and competitive programmers preparing for technical coding interviews. 

Standard interview preparation platforms often lead candidates to practice problems randomly or focus repeatedly on topics they are already comfortable with. AlgoMatch solves this inefficiency by replacing blind problem grinding with data-driven skill targeting.

When a user inputs any public LeetCode username, AlgoMatch automatically executes a multi-stage data processing pipeline:

1. **Real-time Profile Data Ingestion**: Communicates directly with LeetCode's GraphQL API to extract the user's complete problem-solving history, including total solved counts, difficulty breakdown (Easy, Medium, Hard), and distribution across 40+ algorithmic topic tags (such as Dynamic Programming, Graphs, Tries, Binary Search, and Segment Trees).
2. **Normalized Tag Weakness Calculation**: Evaluates relative proficiency across all algorithmic domains. The engine calculates a normalized strength score for each topic relative to the user's most practiced domain, then derives a mathematical weakness coefficient ranging from 0.0 (maximum strength) to 1.0 (unpracticed skill gap).
3. **Precision Catalog Overlap Ranking**: Evaluates a pre-cached catalog of over 3,900 LeetCode problems against the user's specific weakness profile. The algorithm computes a composite weakness match score for every unsolved problem, surfacing the single most impactful question guaranteed to address the user's largest algorithmic gaps.
4. **Interactive Analytics & Recommendation Visualizations**: Presents real-time skill analytics through horizontal priority bars and difficulty distribution donut charts, accompanied by curated problem recommendation cards featuring direct links to solve each challenge on LeetCode.

---

## Detailed Functional Breakdown

### 1. Profile Analysis and Data Extraction
- Scrapes live profile metrics directly from LeetCode's GraphQL backend endpoints.
- Implements exponential backoff retries and HTTP headers to handle rate-limiting.
- Categorizes solved problem metrics across Easy, Medium, and Hard difficulties.

### 2. Algorithmic Weakness Engine
- Computes tag frequency distribution across all solved problems.
- Normalizes topic coverage to identify disproportionately neglected algorithmic patterns.
- Identifies primary skill gaps (such as Iterator, Data Stream, Game Theory, and Trie) and ranks practice priority.

### 3. Problem Recommendation Engine
- Filters out problems already solved by the candidate.
- Computes an aggregate weakness match score (0 to 100) for remaining unsolved catalog problems.
- Provides difficulty-filtered recommendations (All, Easy, Medium, Hard) to allow candidates to practice at their target difficulty level.

### 4. Dual Web Interfaces
- **Single-Page Web Platform**: High-performance HTML/CSS/JS frontend served natively via FastAPI for instant response times on cloud serverless infrastructure (Vercel).
- **Streamlit Analytics Dashboard**: Data application featuring Plotly interactive data visualizations, customizable metrics, and detailed problem inspection panels.

---

## System Structure

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
│       └── problems_catalog.json # Pre-cached Catalog Problems
│
├── frontend/                 # Streamlit Web Application Layer
│   ├── dashboard.py          # Streamlit Organic Forest Green UI Entrypoint
│   └── ui/
│       ├── analytics.py      # Plotly Interactive Visualization
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

---

## Mathematical Scoring Model

### 1. Tag Weakness Score
The system measures relative skill gap in a given topic using:

$$\text{Strength Score}_{\text{tag}} = \frac{\text{Solved Count}_{\text{tag}}}{\max(\text{Solved Counts across all tags})}$$

$$\text{Weakness Score}_{\text{tag}} = 1.0 - \text{Strength Score}_{\text{tag}}$$

- A weakness score of 0.0 represents the user's most practiced algorithmic domain.
- A weakness score of 1.0 represents an unpracticed algorithmic domain.

### 2. Problem Weakness Overlap
Unsolved catalog problems are scored by computing the mean weakness across all associated tags:

$$\text{Problem Score} = \frac{1}{n} \sum_{i=1}^{n} \text{Weakness Score}_{\text{tag}_i}$$

Problems are ranked in descending order of this score to surface the most impactful challenge.

---

## API Reference

All endpoints accept an optional query parameter `?username=<leetcode_username>`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/` | Renders Single-Page Interactive Web Application |
| GET | `/recommend` | Top overall recommended problem |
| GET | `/recommend/easy` | Top Easy recommended problem |
| GET | `/recommend/medium` | Top Medium recommended problem |
| GET | `/recommend/hard` | Top Hard recommended problem |
| GET | `/stats` | User solved counts, percentages, and topic scores |
| POST | `/update` | Purges cache and forces fresh profile scrape |
| POST | `/admin/refresh-catalog` | Triggers background global problem catalog update (`X-Admin-Secret`) |
| GET | `/admin/users` | Fetches logged user telemetry (`X-Admin-Secret`) |

---

## Local Development Setup

### 1. Setup Virtual Environment
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

## Deployment

### Vercel Serverless
1. Import repository on Vercel.
2. Framework Preset: Other.
3. Deploy! Vercel automatically detects `pyproject.toml` and builds the serverless deployment.

### Render Cloud
1. Create a new Blueprint on Render.
2. Connect your repository — Render will automatically launch both `algomatch-api` and `algomatch-dashboard` using `render.yaml`.

---

<div align="center">
  <sub>Built with LeetCode GraphQL API · Machine Learning Weakness Ranking Engine</sub>
</div>
