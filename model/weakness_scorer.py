import json
import os

def load_weakness_map():
    path = os.path.join("data", "processed", "tag_scores.json")
    with open(path, "r") as f:
        tag_scores = json.load(f)

    weakness_map = {}
    for entry in tag_scores:
        tag = entry["tag"].lower().strip()
        weakness_map[tag] = entry["weakness_score"]

    return weakness_map


def score_problem(problem_tags, weakness_map):
    if not problem_tags:
        return 0.0

    scores = []
    for tag in problem_tags:
        tag_name = tag["name"].lower().strip()
        score = weakness_map.get(tag_name, 0.5)
        scores.append(score)

    return round(sum(scores) / len(scores), 4)