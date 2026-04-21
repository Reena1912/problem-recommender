"""
API routes.

Every endpoint accepts an optional `username` query parameter.
When provided, the full scrape → analyse → rank pipeline runs for that user
(results are cached for 10 minutes per user).

If username is omitted the endpoint falls back to the default configured user
(LEETCODE_USERNAME in .env) so existing single-user deployments keep working.
"""

import os
import sys

from fastapi import APIRouter, HTTPException, Query, Request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SESSION_COOKIE, USERNAME
from api.schemas import (
    ProblemRecommendation,
    RecommendationResponse,
    UpdateResponse,
    UserStatsResponse,
)
from api.user_pipeline import run_pipeline

router = APIRouter()


# ── Helpers ────────────────────────────────────────────────────────────────

def _resolve_username(username: str | None) -> str:
    """Use the query-param username, falling back to the env default."""
    resolved = (username or "").strip() or USERNAME
    if not resolved:
        raise HTTPException(
            status_code=400,
            detail=(
                "No username provided. Pass ?username=<your_leetcode_username> "
                "or set LEETCODE_USERNAME in .env."
            ),
        )
    return resolved


def _get_user_data(request: Request, username: str) -> dict:
    """Run the pipeline for the given user, raising HTTP errors on failure."""
    try:
        return run_pipeline(username, request.app.state.all_problems, SESSION_COOKIE)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LeetCode API error: {e}")


def _build_recommendation(problem: dict) -> ProblemRecommendation:
    return ProblemRecommendation(
        title=problem["title"],
        titleSlug=problem["titleSlug"],
        difficulty=problem["difficulty"],
        acceptance_rate=problem["acceptance_rate"],
        tags=problem["tags"],
        weakness_score=problem["weakness_score"],
        leetcode_url=f"https://leetcode.com/problems/{problem['titleSlug']}/",
    )


def _top_weak_tags(weakness_map: dict, n: int = 3) -> list[str]:
    return [
        tag for tag, _ in sorted(weakness_map.items(), key=lambda x: x[1], reverse=True)[:n]
    ]


# ── Endpoints ──────────────────────────────────────────────────────────────

@router.get("/recommend", response_model=RecommendationResponse)
def recommend(
    request: Request,
    username: str | None = Query(default=None, description="LeetCode username"),
):
    user = _resolve_username(username)
    data = _get_user_data(request, user)
    ranked = data["ranked_problems"]

    if not ranked:
        raise HTTPException(status_code=404, detail="No recommendations found.")

    top = ranked[0]
    return RecommendationResponse(
        recommendation=_build_recommendation(top),
        your_weakest_tags=_top_weak_tags(data["weakness_map"]),
        message=f"Based on {user}'s weak areas, start with this {top['difficulty']} problem.",
    )


@router.get("/recommend/{difficulty}", response_model=RecommendationResponse)
def recommend_by_difficulty(
    difficulty: str,
    request: Request,
    username: str | None = Query(default=None, description="LeetCode username"),
):
    valid = ["easy", "medium", "hard"]
    difficulty_clean = difficulty.lower().strip()
    if difficulty_clean not in valid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid difficulty '{difficulty}'. Choose from: easy, medium, hard",
        )

    user = _resolve_username(username)
    data = _get_user_data(request, user)

    filtered = [
        p for p in data["ranked_problems"]
        if p["difficulty"].lower() == difficulty_clean
    ]
    if not filtered:
        raise HTTPException(
            status_code=404,
            detail=f"No {difficulty.capitalize()} problems found for user '{user}'.",
        )

    top = filtered[0]
    return RecommendationResponse(
        recommendation=_build_recommendation(top),
        your_weakest_tags=_top_weak_tags(data["weakness_map"]),
        message=f"Best {difficulty.capitalize()} problem targeting {user}'s weak areas.",
    )


@router.get("/stats", response_model=UserStatsResponse)
def stats(
    request: Request,
    username: str | None = Query(default=None, description="LeetCode username"),
):
    """
    Returns tag scores, solve counts, and totals needed by the dashboard charts.
    Eliminates the need for the dashboard to read local JSON files.
    """
    user = _resolve_username(username)
    data = _get_user_data(request, user)

    return UserStatsResponse(
        username=user,
        solve_counts=data["solve_counts"],
        total_available=data["total_available"],
        tag_scores=data["tag_scores"],
    )


@router.post("/update", response_model=UpdateResponse)
def update(
    request: Request,
    username: str | None = Query(default=None, description="LeetCode username"),
):
    """
    Force a cache refresh for a user (bypasses the 10-minute TTL).
    Useful after solving new problems.
    """
    from api.user_pipeline import _cache  # clear the specific user entry

    user = _resolve_username(username)
    _cache.pop(user, None)  # invalidate so run_pipeline re-fetches

    data = _get_user_data(request, user)
    top = data["ranked_problems"][0] if data["ranked_problems"] else None

    return UpdateResponse(
        success=True,
        message=f"Data refreshed for user '{user}'.",
        top_recommendation=top["title"] if top else None,
    )