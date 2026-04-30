"""
api/tracker.py

Saves every user's LeetCode username + full stats to Supabase.
Uses service_role key which bypasses RLS.
"""

import os
from datetime import datetime, timezone

_last_error: str = "none"   # readable via /admin/tracker-status


def _make_client():
    """Create a fresh Supabase client — not cached, avoids stale state."""
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_SERVICE_KEY", "").strip()
    if not url or not key:
        return None
    from supabase import create_client
    return create_client(url, key)


def log_user(username: str, pipeline_result: dict) -> None:
    global _last_error
    try:
        client = _make_client()
        if client is None:
            _last_error = "SUPABASE_URL or SUPABASE_SERVICE_KEY not set"
            print(f"[tracker] {_last_error}")
            return

        sc = pipeline_result.get("solve_counts", {})
        ta = pipeline_result.get("total_available", {})
        ts = pipeline_result.get("tag_scores", [])

        # Convert to plain lists of strings (safe for Postgres TEXT[] columns)
        weakest   = [str(t["tag"]) for t in ts[:5]]
        strongest = [str(t["tag"]) for t in reversed(ts[-5:])]

        top = None
        if pipeline_result.get("ranked_problems"):
            top = pipeline_result["ranked_problems"][0]["title"]

        row = {
            "username":           username,
            "last_seen":          datetime.now(timezone.utc).isoformat(),
            "solved_total":       int(sc.get("All",    0)),
            "solved_easy":        int(sc.get("Easy",   0)),
            "solved_medium":      int(sc.get("Medium", 0)),
            "solved_hard":        int(sc.get("Hard",   0)),
            "total_easy":         int(ta.get("Easy",   0)),
            "total_medium":       int(ta.get("Medium", 0)),
            "total_hard":         int(ta.get("Hard",   0)),
            "weakest_tags":       weakest,
            "strongest_tags":     strongest,
            "top_recommendation": top,
        }

        res = client.table("users").upsert(row).execute()
        _last_error = "none"
        print(f"[tracker] OK — logged '{username}'  rows={len(res.data)}")

    except Exception as e:
        _last_error = str(e)
        print(f"[tracker] FAILED for '{username}': {e}")


def get_all_users() -> list[dict]:
    try:
        client = _make_client()
        if client is None:
            return []
        res = client.table("users").select("*").order("last_seen", desc=True).execute()
        return res.data or []
    except Exception as e:
        print(f"[tracker] get_all_users failed: {e}")
        return []


def get_user(username: str) -> dict | None:
    try:
        client = _make_client()
        if client is None:
            return None
        res = client.table("users").select("*").eq("username", username).limit(1).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        print(f"[tracker] get_user failed: {e}")
        return None


def get_last_error() -> str:
    return _last_error