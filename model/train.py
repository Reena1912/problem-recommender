import json
import os
import sys
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.weakness_scorer import load_weakness_map
from model.problem_ranker import rank_problems


def train():
    print("Loading weakness map...")
    weakness_map = load_weakness_map()

    print("Ranking problems...")
    ranked_problems = rank_problems()

    model_data = {
        "weakness_map": weakness_map,
        "ranked_problems": ranked_problems,
    }

    os.makedirs("model", exist_ok=True)
    joblib.dump(model_data, "model/model.pkl")

    print(f"\nmodel.pkl saved — {len(ranked_problems)} problems ranked")
    print(f"Top recommendation: {ranked_problems[0]['title']} ({ranked_problems[0]['difficulty']})")


if __name__ == "__main__":
    train()