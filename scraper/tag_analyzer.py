import json
import os

def analyze_tags():
    with open("data/processed/problems_clean.json", "r") as f:
        data = json.load(f)

    tags = data["tags"]

    if not tags:
        print("No tag data found.")
        return

    max_solved = max(tag["solved"] for tag in tags)

    tag_scores = []
    for tag in tags:
        if max_solved == 0:
            strength = 0.0
        else:
            strength = tag["solved"] / max_solved

        weakness = round(1 - strength, 4)

        tag_scores.append({
            "tag": tag["tag"],
            "solved": tag["solved"],
            "strength_score": round(strength, 4),
            "weakness_score": weakness
        })

    tag_scores.sort(key=lambda x: x["weakness_score"], reverse=True)

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