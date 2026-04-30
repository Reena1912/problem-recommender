"""

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
from api.tracker import log_user, get_all_users, get_user   # ← new

router = APIRouter()


# ── Helpers ────────────────────────────────────────────────────────────────

def _resolve_username(username: str | None) -> str:
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
        from api.tracker import log_user
        data = run_pipeline(username, request.app.state.all_problems, SESSION_COOKIE)
        log_user(username, data)   # ← saves user to Supabase
        return data
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


# ── Main Endpoints ─────────────────────────────────────────────────────────

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
    from api.user_pipeline import _cache

    user = _resolve_username(username)
    _cache.pop(user, None)

    data = _get_user_data(request, user)
    top = data["ranked_problems"][0] if data["ranked_problems"] else None

    return UpdateResponse(
        success=True,
        message=f"Data refreshed for user '{user}'.",
        top_recommendation=top["title"] if top else None,
    )


# ── Admin Endpoints ────────────────────────────────────────────────────────

@router.get("/admin/users")
def admin_all_users(secret: str = Query(description="Admin secret key")):
    """
    Returns every user who has ever used the app.
    Requires ?secret=<ADMIN_SECRET> (set this in your .env / Render env vars).
    """
    expected = os.getenv("ADMIN_SECRET", "")
    if not expected or secret != expected:
        raise HTTPException(status_code=403, detail="Invalid or missing admin secret.")

    users = get_all_users()
    return {
        "total_users": len(users),
        "users": users,
    }


@router.get("/admin/users/{username}")
def admin_single_user(username: str, secret: str = Query(description="Admin secret key")):
    """
    Returns saved stats for a specific LeetCode username.
    Requires ?secret=<ADMIN_SECRET>.
    """
    expected = os.getenv("ADMIN_SECRET", "")
    if not expected or secret != expected:
        raise HTTPException(status_code=403, detail="Invalid or missing admin secret.")

    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail=f"No data found for '{username}'.")
    return user

@router.get("/admin/debug")
def admin_debug(secret: str = Query()):
    expected = os.getenv("ADMIN_SECRET", "")
    if not expected or secret != expected:
        raise HTTPException(status_code=403, detail="Invalid secret.")

    result = {
        "env_vars": {
            "SUPABASE_URL_set":          bool(os.getenv("SUPABASE_URL")),
            "SUPABASE_SERVICE_KEY_set":  bool(os.getenv("SUPABASE_SERVICE_KEY")),
            "ADMIN_SECRET_set":          bool(os.getenv("ADMIN_SECRET")),
        },
        "supabase_import": None,
        "supabase_connect": None,
        "supabase_query": None,
        "tracker_log_test": None,
        "error": None,
    }

    # Step 1 — can we import supabase?
    try:
        from supabase import create_client
        result["supabase_import"] = "OK"
    except Exception as e:
        result["supabase_import"] = f"FAILED: {e}"
        result["error"] = "supabase package not installed"
        return result

    # Step 2 — can we connect?
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        client = create_client(url, key)
        result["supabase_connect"] = "OK"
    except Exception as e:
        result["supabase_connect"] = f"FAILED: {e}"
        result["error"] = "Bad URL or SERVICE_KEY"
        return result

    # Step 3 — can we query the users table?
    try:
        res = client.table("users").select("count", count="exact").execute()
        result["supabase_query"] = f"OK — {res.count} rows in users table"
    except Exception as e:
        result["supabase_query"] = f"FAILED: {e}"
        result["error"] = "Table doesnt exist or RLS is blocking service_role (unusual)"
        return result

    # Step 4 — does tracker.log_user work end to end?
    try:
        from api.tracker import log_user
        log_user("__debug_test__", {
            "solve_counts":    {"All": 0, "Easy": 0, "Medium": 0, "Hard": 0},
            "total_available": {"All": 0, "Easy": 0, "Medium": 0, "Hard": 0},
            "tag_scores":      [],
            "ranked_problems": [],
        })
        result["tracker_log_test"] = "OK — test row written"
    except Exception as e:
        result["tracker_log_test"] = f"FAILED: {e}"
        result["error"] = "tracker.log_user threw an exception"

    return result
@router.get("/admin/test-write")
def admin_test_write(secret: str = Query()):
    expected = os.getenv("ADMIN_SECRET", "")
    if not expected or secret != expected:
        raise HTTPException(status_code=403, detail="Invalid secret.")

    from supabase import create_client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    client = create_client(url, key)

    # Write — no try/except so the real error surfaces
    write = client.table("users").upsert({
        "username":           "__test__",
        "solved_total":       1,
        "weakest_tags":       ["Array"],
        "strongest_tags":     ["HashMap"],
        "top_recommendation": "Two Sum"
    }, on_conflict="username").execute()

    # Read it back to confirm
    read = client.table("users").select("*").eq("username", "__test__").execute()

    return {
        "write_data": write.data,
        "read_back":  read.data,
    }
    
    @router.get("/admin/tracker-status")
def tracker_status(secret: str = Query()):
    expected = os.getenv("ADMIN_SECRET", "")
    if not expected or secret != expected:
        raise HTTPException(status_code=403, detail="Invalid secret.")
    from api.tracker import get_last_error
    return {"last_tracker_error": get_last_error()}
