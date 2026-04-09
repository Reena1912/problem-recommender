import requests
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SESSION_COOKIE, USERNAME

GRAPHQL_URL = "https://leetcode.com/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "Cookie": f"LEETCODE_SESSION={SESSION_COOKIE}",
}

QUERY = """
query userSolvedProblems($username: String!) {
  matchedUser(username: $username) {
    submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
    tagProblemCounts {
      advanced {
        tagName
        problemsSolved
      }
      intermediate {
        tagName
        problemsSolved
      }
      fundamental {
        tagName
        problemsSolved
      }
    }
  }
  allQuestionsCount {
    difficulty
    count
  }
}
"""

def fetch_profile():
    payload = {
        "query": QUERY,
        "variables": {"username": USERNAME}
    }

    response = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)

    if response.status_code != 200:
        print(f"Request failed: {response.status_code}")
        print(response.text)
        return

    data = response.json()

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/profile_raw.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Saved to data/raw/profile_raw.json")

ALL_PROBLEMS_QUERY = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total: totalNum
    questions: data {
      title
      titleSlug
      difficulty
      acRate
      topicTags {
        name
        slug
      }
    }
  }
}
"""

def fetch_all_problems():
    all_questions = []
    skip = 0
    limit = 100

    while True:
        payload = {
            "query": ALL_PROBLEMS_QUERY,
            "variables": {
                "categorySlug": "",
                "limit": limit,
                "skip": skip,
                "filters": {}
            }
        }

        response = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)

        if response.status_code != 200:
            print(f"Failed at skip={skip}: {response.status_code}")
            break

        data = response.json()
        questions = data["data"]["problemsetQuestionList"]["questions"]
        total = data["data"]["problemsetQuestionList"]["total"]

        all_questions.extend(questions)
        print(f"Fetched {len(all_questions)}/{total} problems...")

        if len(all_questions) >= total:
            break

        skip += limit

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/all_problems_raw.json", "w") as f:
        json.dump(all_questions, f, indent=2)

    print(f"Saved {len(all_questions)} problems to data/raw/all_problems_raw.json")

SOLVED_PROBLEMS_QUERY = """
query userSolvedProblemsDetail($username: String!) {
  matchedUser(username: $username) {
    problemsSolvedBeatsStats {
      difficulty
      percentage
    }
    submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
  recentAcSubmissionList(username: $username, limit: 50) {
    titleSlug
  }
}
"""

def fetch_solved_slugs():
    payload = {
        "query": SOLVED_PROBLEMS_QUERY,
        "variables": {"username": USERNAME}
    }

    response = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    data = response.json()

    recent = data["data"]["recentAcSubmissionList"]
    slugs = [item["titleSlug"] for item in recent]

    with open("data/raw/solved_slugs.json", "w") as f:
        json.dump(slugs, f, indent=2)

    print(f"Saved {len(slugs)} solved slugs")
    
if __name__ == "__main__":
    fetch_profile()
    fetch_all_problems()
    fetch_solved_slugs()