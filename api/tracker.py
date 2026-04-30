"""

Saves every user's LeetCode username + full stats to Supabase.
Never raises — analytics must never crash the main app.
"""

import os
from datetime import datetime, timezone

_client = None


def _get_client():
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL")
        # Use service_role key — bypasses RLS so the backend has full access.
        # NEVER expose this key in the browser or frontend code.
        key = os.getenv("SUPABASE_SERVICE_KEY")
        if not url or not key:
            return None
        from supabase import create_client
        _client = create_client(url, key)
    return _client


def log_user(username: str, pipeline_result: dict) -> None:
    """
    Upsert one row per username so you always have their latest stats.
    Called automatically after every successful pipeline run.
    """
    try:
        client = _get_client()
        if client is None:
            return

        sc  = pipeline_result.get("solve_counts", {})
        ta  = pipeline_result.get("total_available", {})
        ts  = pipeline_result.get("tag_scores", [])

        # Top 5 weakest & strongest tags
        weakest   = [t["tag"] for t in ts[:5]]
        strongest = [t["tag"] for t in reversed(ts[-5:])]

        row = {
            "username":        username,
            "last_seen":       datetime.now(timezone.utc).isoformat(),
            "solved_total":    sc.get("All",    0),
            "solved_easy":     sc.get("Easy",   0),
            "solved_medium":   sc.get("Medium", 0),
            "solved_hard":     sc.get("Hard",   0),
            "total_easy":      ta.get("Easy",   0),
            "total_medium":    ta.get("Medium", 0),
            "total_hard":      ta.get("Hard",   0),
            "weakest_tags":    weakest,
            "strongest_tags":  strongest,
            "top_recommendation": (
                pipeline_result["ranked_problems"][0]["title"]
                if pipeline_result.get("ranked_problems") else None
            ),
        }

        # upsert — insert on first visit, update on repeat visits
        client.table("users").upsert(row, on_conflict="username").execute()

    except Exception as e:
        print(f"[tracker] Non-fatal error logging user '{username}': {e}")


def get_all_users() -> list[dict]:
    """Return all tracked users, newest first."""
    try:
        client = _get_client()
        if client is None:
            return []
        res = (
            client.table("users")
            .select("*")
            .order("last_seen", desc=True)
            .execute()
        )
        return res.data or []
    except Exception as e:
        print(f"[tracker] Could not fetch users: {e}")
        return []


def get_user(username: str) -> dict | None:
    """Return a single user's saved stats."""
    try:
        client = _get_client()
        if client is None:
            return None
        res = (
            client.table("users")
            .select("*")
            .eq("username", username)
            .limit(1)
            .execute()
        )
        return res.data[0] if res.data else None
    except Exception as e:
        print(f"[tracker] Could not fetch user '{username}': {e}")
        return None