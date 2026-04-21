"""
Data normalization for raw LeetCode API responses.

parse_profile_data() is the primary public function — it works entirely
in memory so it can be called for any user without touching the filesystem.

The file-based parse_profile() wrapper is kept for standalone script use.
"""

import json
import os


def parse_profile_data(raw: dict) -> dict:
    """
    Parse a raw profile API response into a clean structured dict.

    Returns:
        {
            "solve_counts":    {"All": n, "Easy": n, "Medium": n, "Hard": n},
            "total_available": {"All": n, "Easy": n, "Medium": n, "Hard": n},
            "tags":            [{"tag": str, "solved": int}, ...]
        }
    """
    user_data = raw["data"]["matchedUser"]
    total_counts = {
        item["difficulty"]: item["count"]
        for item in raw["data"]["allQuestionsCount"]
    }

    tag_sections = user_data["tagProblemCounts"]
    all_tags = (
        tag_sections["fundamental"]
        + tag_sections["intermediate"]
        + tag_sections["advanced"]
    )

    cleaned_tags = [
        {"tag": tag["tagName"], "solved": tag["problemsSolved"]}
        for tag in all_tags
    ]

    solve_counts = {
        item["difficulty"]: item["count"]
        for item in user_data["submitStatsGlobal"]["acSubmissionNum"]
    }

    return {
        "solve_counts": solve_counts,
        "total_available": total_counts,
        "tags": cleaned_tags,
    }


# ── Legacy file-based wrapper ──────────────────────────────────────────────

def parse_profile():
    with open("data/raw/profile_raw.json", "r") as f:
        raw = json.load(f)

    output = parse_profile_data(raw)

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/problems_clean.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Saved to data/processed/problems_clean.json")


if __name__ == "__main__":
    parse_profile()