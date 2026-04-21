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


def analyze_tags():
    with open("data/processed/problems_clean.json", "r") as f:
        data = json.load(f)

    tag_scores = compute_tag_scores(data["tags"])

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/tag_scores.json", "w") as f:
        json.dump(tag_scores, f, indent=2)

    print("\nYour weakest areas:")
    for t in tag_scores[:5]:
        print(f"  {t['tag']}: weakness={t['weakness_score']}, solved={t['solved']}")

    print("\nYour strongest areas:")
    for t in tag_scores[-5:]:
        print(f"  {t['tag']}: weakness={t['weakness_score']}, solved={t['solved']}")

    print("\nSaved to data/processed/tag_scores.json")


if __name__ == "__main__":
    analyze_tags()