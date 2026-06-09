import json
import os


def compute_tag_scores(tags: list) -> list:
    if not tags:
        return []

    max_solved = max(t["solved"] for t in tags)

    scored = []
    for tag in tags:
        strength = (tag["solved"] / max_solved) if max_solved > 0 else 0.0
        scored.append({
            "tag": tag["tag"],
            "solved": tag["solved"],
            "strength_score": round(strength, 4),
            "weakness_score": round(1 - strength, 4),
        })

    scored.sort(key=lambda x: x["weakness_score"], reverse=True)
    return scored