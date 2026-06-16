import requests
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SESSION_COOKIE, USERNAME

GRAPHQL_URL = "https://leetcode.com/graphql"


import time

def _make_headers(session_cookie: str) -> dict:
    return {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": f"LEETCODE_SESSION={session_cookie}" if session_cookie else "",
    }


def _post_with_retry(url: str, json_data: dict, headers: dict, max_retries: int = 5, initial_backoff: float = 1.0) -> requests.Response:
    backoff = initial_backoff
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=json_data, headers=headers, timeout=15)
            # If rate-limited (429) or server error (5xx), we wait and retry
            if response.status_code == 429 or 500 <= response.status_code < 600:
                print(f"  [WARNING] HTTP {response.status_code} on attempt {attempt + 1}. Retrying in {backoff:.2f}s...")
                time.sleep(backoff)
                backoff *= 2
                continue
            return response
        except (requests.exceptions.RequestException, ConnectionError) as e:
            if attempt == max_retries - 1:
                raise
            print(f"  [WARNING] Connection error on attempt {attempt + 1}: {e}. Retrying in {backoff:.2f}s...")
            time.sleep(backoff)
            backoff *= 2
    # Try one last time synchronously as fallback
    return requests.post(url, json=json_data, headers=headers, timeout=15)


PROFILE_QUERY = """
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

SOLVED_PROBLEMS_QUERY = """
query userSolvedProblemsDetail($username: String!) {
  matchedUser(username: $username) {
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


def fetch_user_profile_data(username: str, session_cookie: str) -> dict:
    payload = {"query": PROFILE_QUERY, "variables": {"username": username}}
    response = _post_with_retry(
        GRAPHQL_URL, json_data=payload, headers=_make_headers(session_cookie)
    )
    if response.status_code != 200:
        raise ConnectionError(
            f"Profile fetch failed for '{username}': HTTP {response.status_code}"
        )
    return response.json()


def fetch_solved_slugs_data(username: str, session_cookie: str) -> list[str]:
    payload = {
        "query": SOLVED_PROBLEMS_QUERY,
        "variables": {"username": username},
    }
    response = _post_with_retry(
        GRAPHQL_URL, json_data=payload, headers=_make_headers(session_cookie)
    )
    data = response.json()
    recent = data["data"]["recentAcSubmissionList"]
    return [item["titleSlug"] for item in recent]


def fetch_all_problems_data(session_cookie: str) -> list[dict]:
    all_questions: list[dict] = []
    skip = 0
    limit = 100

    while True:
        payload = {
            "query": ALL_PROBLEMS_QUERY,
            "variables": {
                "categorySlug": "",
                "limit": limit,
                "skip": skip,
                "filters": {},
            },
        }
        response = _post_with_retry(
            GRAPHQL_URL, json_data=payload, headers=_make_headers(session_cookie)
        )
        if response.status_code != 200:
            raise ConnectionError(
                f"Problem catalog fetch failed at skip={skip}: HTTP {response.status_code}"
            )

        data = response.json()
        questions = data["data"]["problemsetQuestionList"]["questions"]
        total = data["data"]["problemsetQuestionList"]["total"]
        all_questions.extend(questions)

        print(f"  Fetched {len(all_questions)}/{total} problems...")
        if len(all_questions) >= total:
            break
        skip += limit

    return all_questions