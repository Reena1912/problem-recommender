import os
import sys
import subprocess
from fastapi import APIRouter, HTTPException, Request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.schemas import RecommendationResponse, ProblemRecommendation, UpdateResponse

router = APIRouter()


def build_recommendation(problem: dict) -> ProblemRecommendation:
    return ProblemRecommendation(
        title=problem["title"],
        titleSlug=problem["titleSlug"],
        difficulty=problem["difficulty"],
        acceptance_rate=problem["acceptance_rate"],
        tags=problem["tags"],
        weakness_score=problem["weakness_score"],
        leetcode_url=f"https://leetcode.com/problems/{problem['titleSlug']}/"
    )


def get_top_weak_tags(weakness_map: dict, n: int = 3) -> list:
    sorted_tags = sorted(weakness_map.items(), key=lambda x: x[1], reverse=True)
    return [tag for tag, score in sorted_tags[:n]]


@router.get("/recommend", response_model=RecommendationResponse)
def recommend(request: Request):
    ranked = request.app.state.ranked_problems

    if not ranked:
        raise HTTPException(status_code=404, detail="No recommendations available. Run /update first.")

    top = ranked[0]
    weakness_map = request.app.state.weakness_map

    return RecommendationResponse(
        recommendation=build_recommendation(top),
        your_weakest_tags=get_top_weak_tags(weakness_map),
        message=f"Based on your weak areas, start with this {top['difficulty']} problem."
    )


@router.get("/recommend/{difficulty}", response_model=RecommendationResponse)
def recommend_by_difficulty(difficulty: str, request: Request):
    valid = ["easy", "medium", "hard"]
    difficulty_clean = difficulty.lower().strip()

    if difficulty_clean not in valid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid difficulty. Choose from: Easy, Medium, Hard"
        )

    ranked = request.app.state.ranked_problems
    filtered = [
        p for p in ranked
        if p["difficulty"].lower() == difficulty_clean
    ]

    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No {difficulty} problems found in recommendations."
        )

    top = filtered[0]
    weakness_map = request.app.state.weakness_map

    return RecommendationResponse(
        recommendation=build_recommendation(top),
        your_weakest_tags=get_top_weak_tags(weakness_map),
        message=f"Best {difficulty.capitalize()} problem targeting your weak areas."
    )


@router.post("/update", response_model=UpdateResponse)
def update(request: Request):
    try:
        print("Re-fetching LeetCode data...")
        subprocess.run(
            [sys.executable, "scraper/fetch_profile.py"],
            check=True
        )

        print("Retraining model...")
        subprocess.run(
            [sys.executable, "model/train.py"],
            check=True
        )

        import joblib
        model_data = joblib.load("model/model.pkl")
        request.app.state.ranked_problems = model_data["ranked_problems"]
        request.app.state.weakness_map = model_data["weakness_map"]

        top = request.app.state.ranked_problems[0]

        return UpdateResponse(
            success=True,
            message="Model updated successfully with fresh LeetCode data.",
            top_recommendation=top["title"]
        )

    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Update failed during subprocess: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Update failed: {str(e)}"
        )