"""
FastAPI application entry point.
  • The global problem catalog (all_problems) is fetched once at startup and
    shared across all requests — it's the same for every user.
  • The pre-trained model.pkl is no longer required; per-user analysis runs
    on demand via user_pipeline.run_pipeline().
  • If model.pkl exists it is still loaded so existing single-user setups
    keep working without re-running any scripts.
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SESSION_COOKIE
from scraper.fetch_profile import fetch_all_problems_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Fetching LeetCode problem catalog (this takes ~10 s)…")
    app.state.all_problems = fetch_all_problems_data(SESSION_COOKIE)
    print(f"  ✓ {len(app.state.all_problems)} problems loaded")

    # Backwards-compat: load pre-trained model if present
    model_path = os.path.join("model", "model.pkl")
    if os.path.exists(model_path):
        import joblib
        model_data = joblib.load(model_path)
        app.state.default_ranked = model_data.get("ranked_problems", [])
        app.state.default_weakness = model_data.get("weakness_map", {})
        print(f"  ✓ model.pkl loaded ({len(app.state.default_ranked)} ranked problems)")
    else:
        app.state.default_ranked = []
        app.state.default_weakness = {}
        print("  ℹ  No model.pkl found — per-user analysis will run on demand")

    yield

    print("Server shutting down")


app = FastAPI(
    title="LeetCode Recommender API",
    description=(
        "Recommends the best LeetCode problem for any user based on their weak areas. "
        "Pass ?username=<leetcode_username> to every endpoint."
    ),
    
    version="2.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
from api.routes import router  # noqa: E402 (import after app is defined)
app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "LeetCode Recommender API",
        "usage": "Add ?username=your_leetcode_username to any endpoint",
        "endpoints": {
            "recommend (any difficulty)": "/recommend?username=<user>",
            "recommend by difficulty":    "/recommend/{easy|medium|hard}?username=<user>",
            "stats (charts data)":        "/stats?username=<user>",
            "docs":                        "/docs",
        },
    }