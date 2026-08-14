import json
import os


def parse_profile_data(raw: dict) -> dict:
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