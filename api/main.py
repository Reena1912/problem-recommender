from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = os.path.join("model", "model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            "model.pkl not found. Run model/train.py first."
        )

    model_data = joblib.load(model_path)
    app.state.ranked_problems = model_data["ranked_problems"]
    app.state.weakness_map = model_data["weakness_map"]

    print(f"Model loaded — {len(app.state.ranked_problems)} problems ranked")
    print(f"Top recommendation: {app.state.ranked_problems[0]['title']}")

    yield

    print("Server shutting down")


app = FastAPI(
    title="LeetCode Recommender API",
    description="Recommends the best LeetCode problem to solve based on your weak areas",
    version="1.0.0",
    lifespan=lifespan
)

from api.routes import router
app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "LeetCode Recommender API",
        "endpoints": {
            "recommend": "/recommend",
            "recommend_by_difficulty": "/recommend/{difficulty}",
            "update": "/update (POST)",
            "docs": "/docs"
        }
    }
    