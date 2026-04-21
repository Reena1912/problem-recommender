"""
Per-user analysis pipeline.

Orchestrates: fetch profile → parse → score → rank → return.
Results are cached in memory (TTL = CACHE_TTL_SECONDS) so repeated
dashboard refreshes don't hammer the LeetCode API.
"""

import time
from scraper.fetch_profile import fetch_user_profile_data, fetch_solved_slugs_data
from scraper.parse_submissions import parse_profile_data
from scraper.tag_analyzer import compute_tag_scores
from model.weakness_scorer import score_problem

CACHE_TTL_SECONDS = 600  # 10 minutes

# { username -> {"data": {...}, "expires_at": float} }
_cache: dict = {}


def _is_cached(username: str) -> bool:
    entry = _cache.get(username)
    return entry is not None and time.time() < entry["expires_at"]


def _get_cached(username: str) -> dict:
    return _cache[username]["data"]


def _set_cache(username: str, data: dict) -> None:
    _cache[username] = {
        "data": data,
        "expires_at": time.time() + CACHE_TTL_SECONDS,
    }


def run_pipeline(username: str, all_problems: list, session_cookie: str) -> dict:
    """
    Full pipeline for a given LeetCode username.
    Returns a dict with: ranked_problems, weakness_map, tag_scores,
    solve_counts, total_available.

    Raises ValueError if the username is not found on LeetCode.
    """
    if _is_cached(username):
        return _get_cached(username)

    # 1. Fetch profile & solved slugs from LeetCode
    profile_raw = fetch_user_profile_data(username, session_cookie)

    if profile_raw.get("data", {}).get("matchedUser") is None:
        raise ValueError(f"LeetCode user '{username}' not found.")

    solved_slugs = set(fetch_solved_slugs_data(username, session_cookie))

    # 2. Parse profile into structured form
    parsed = parse_profile_data(profile_raw)

    # 3. Score each tag
    tag_scores = compute_tag_scores(parsed["tags"])
    weakness_map = {
        t["tag"].lower().strip(): t["weakness_score"] for t in tag_scores
    }

    # 4. Rank unsolved problems by how well they target weak areas
    ranked = []
    for problem in all_problems:
        if problem["titleSlug"] in solved_slugs:
            continue

        ws = score_problem(problem["topicTags"], weakness_map)
        ranked.append({
            "title": problem["title"],
            "titleSlug": problem["titleSlug"],
            "difficulty": problem["difficulty"],
            "acceptance_rate": round(problem["acRate"], 2),
            "tags": [t["name"] for t in problem["topicTags"]],
            "weakness_score": ws,
        })

    ranked.sort(key=lambda x: x["weakness_score"], reverse=True)

    result = {
        "ranked_problems": ranked,
        "weakness_map": weakness_map,
        "tag_scores": tag_scores,
        "solve_counts": parsed["solve_counts"],
        "total_available": parsed["total_available"],
    }

    _set_cache(username, result)
    return result