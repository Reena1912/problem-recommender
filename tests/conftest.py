import os
import sys
from pathlib import Path

# Add backend directory to python path for pytest execution
backend_dir = str(Path(__file__).parent.parent / "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import pytest
from fastapi.testclient import TestClient
from api.main import app

@pytest.fixture
def mock_problems_catalog():
    """Mock problem catalog list containing Easy, Medium, and Hard samples."""
    return [
        {
            "title": "Two Sum",
            "titleSlug": "two-sum",
            "difficulty": "Easy",
            "acRate": 49.5,
            "topicTags": [{"name": "Array", "slug": "array"}]
        },
        {
            "title": "Longest Substring Without Repeating Characters",
            "titleSlug": "longest-substring-without-repeating-characters",
            "difficulty": "Medium",
            "acRate": 33.8,
            "topicTags": [{"name": "Hash Table", "slug": "hash-table"}, {"name": "Sliding Window", "slug": "sliding-window"}]
        },
        {
            "title": "Median of Two Sorted Arrays",
            "titleSlug": "median-of-two-sorted-arrays",
            "difficulty": "Hard",
            "acRate": 37.1,
            "topicTags": [{"name": "Array", "slug": "array"}, {"name": "Binary Search", "slug": "binary-search"}]
        },
        {
            "title": "Edit Distance",
            "titleSlug": "edit-distance",
            "difficulty": "Hard",
            "acRate": 52.4,
            "topicTags": [{"name": "Dynamic Programming", "slug": "dynamic-programming"}]
        }
    ]

@pytest.fixture
def mock_user_profile_data():
    """Mock user profile GraphQL raw API response."""
    return {
        "data": {
            "matchedUser": {
                "submitStatsGlobal": {
                    "acSubmissionNum": [
                        {"difficulty": "All", "count": 1},
                        {"difficulty": "Easy", "count": 1},
                        {"difficulty": "Medium", "count": 0},
                        {"difficulty": "Hard", "count": 0}
                    ]
                },
                "tagProblemCounts": {
                    "fundamental": [
                        {"tagName": "Array", "problemsSolved": 1}
                    ],
                    "intermediate": [
                        {"tagName": "Hash Table", "problemsSolved": 0},
                        {"tagName": "Sliding Window", "problemsSolved": 0}
                    ],
                    "advanced": [
                        {"tagName": "Dynamic Programming", "problemsSolved": 0}
                    ]
                }
            },
            "allQuestionsCount": [
                {"difficulty": "All", "count": 3000},
                {"difficulty": "Easy", "count": 800},
                {"difficulty": "Medium", "count": 1400},
                {"difficulty": "Hard", "count": 800}
            ]
        }
    }

@pytest.fixture
def mock_solved_slugs():
    """Mock list of user's solved LeetCode problem slugs."""
    return ["two-sum"]

@pytest.fixture
def test_client(mock_problems_catalog):
    """Fixture creating a FastAPI test client with mocked state catalog."""
    app.state.all_problems = mock_problems_catalog
    with TestClient(app) as client:
        yield client
