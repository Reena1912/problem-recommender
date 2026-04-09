import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.weakness_scorer import load_weakness_map, score_problem


def rank_problems():
    with open("data/raw/all_problems_raw.json", "r") as f:
        all_problems = json.load(f)

    with open("data/raw/solved_slugs.json", "r") as f:
        solved_slugs = set(json.load(f))

    weakness_map = load_weakness_map()

    ranked = []
    for problem in all_problems:
        if problem["titleSlug"] in solved_slugs:
            continue

        weakness_score = score_problem(problem["topicTags"], weakness_map)

        ranked.append({
            "title": problem["title"],
            "titleSlug": problem["titleSlug"],
            "difficulty": problem["difficulty"],
            "acceptance_rate": round(problem["acRate"], 2),
            "tags": [t["name"] for t in problem["topicTags"]],
            "weakness_score": weakness_score
        })

    ranked.sort(key=lambda x: x["weakness_score"], reverse=True)

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/ranked_problems.json", "w") as f:
        json.dump(ranked, f, indent=2)

    print(f"\nTop 5 recommended problems for you:")
    for i, p in enumerate(ranked[:5], 1):
        print(f"  {i}. {p['title']} ({p['difficulty']}) — weakness score: {p['weakness_score']}")
        print(f"     Tags: {', '.join(p['tags'])}")

    print(f"\nSaved {len(ranked)} ranked problems to data/processed/ranked_problems.json")
    return ranked


if __name__ == "__main__":
    rank_problems()