import json
import os

def parse_profile():
    with open("data/raw/profile_raw.json", "r") as f:
        raw = json.load(f)

    user_data = raw["data"]["matchedUser"]
    total_counts = {item["difficulty"]: item["count"] for item in raw["data"]["allQuestionsCount"]}

    tag_sections = user_data["tagProblemCounts"]
    all_tags = (
        tag_sections["fundamental"] +
        tag_sections["intermediate"] +
        tag_sections["advanced"]
    )

    cleaned_tags = []
    for tag in all_tags:
        cleaned_tags.append({
            "tag": tag["tagName"],
            "solved": tag["problemsSolved"]
        })

    solve_counts = {
        item["difficulty"]: item["count"]
        for item in user_data["submitStatsGlobal"]["acSubmissionNum"]
    }

    output = {
        "solve_counts": solve_counts,
        "total_available": total_counts,
        "tags": cleaned_tags
    }

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/problems_clean.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Saved to data/processed/problems_clean.json")
    
def get_solved_slugs():
    with open("data/raw/profile_raw.json", "r") as f:
        raw = json.load(f)
    
    solved = set()
    user_data = raw["data"]["matchedUser"]
    
    for section in user_data["tagProblemCounts"].values():
        for tag in section:
            pass
    
    return solved

if __name__ == "__main__":
    parse_profile()