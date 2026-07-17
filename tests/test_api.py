from unittest.mock import patch
import pytest

@pytest.fixture
def mock_pipeline_result():
    """Mock result dictionary returned by run_pipeline."""
    return {
        "ranked_problems": [
            {
                "title": "Edit Distance",
                "titleSlug": "edit-distance",
                "difficulty": "Hard",
                "acRate": 52.4,  # user_pipeline returns acRate -> routes normalizes it
                "acceptance_rate": 52.4,
                "tags": ["Dynamic Programming"],
                "weakness_score": 0.98
            },
            {
                "title": "Longest Substring Without Repeating Characters",
                "titleSlug": "longest-substring-without-repeating-characters",
                "difficulty": "Medium",
                "acRate": 33.8,
                "acceptance_rate": 33.8,
                "tags": ["Hash Table", "Sliding Window"],
                "weakness_score": 0.85
            }
        ],
        "weakness_map": {
            "dynamic-programming": 0.98,
            "sliding-window": 0.85,
            "hash-table": 0.85
        },
        "tag_scores": [
            {"tag": "Dynamic Programming", "solved": 0, "strength_score": 0.0, "weakness_score": 0.98},
            {"tag": "Sliding Window", "solved": 0, "strength_score": 0.0, "weakness_score": 0.85},
            {"tag": "Hash Table", "solved": 0, "strength_score": 0.0, "weakness_score": 0.85}
        ],
        "solve_counts": {"All": 10, "Easy": 5, "Medium": 3, "Hard": 2},
        "total_available": {"All": 3000, "Easy": 800, "Medium": 1400, "Hard": 800}
    }

def test_root_endpoint(test_client):
    """Test the root endpoint returns API status and usage info."""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data

def test_recommend_success(test_client, mock_pipeline_result):
    """Test the general /recommend endpoint returns top priority recommendation."""
    with patch("api.routes.run_pipeline", return_value=mock_pipeline_result):
        response = test_client.get("/recommend?username=test_coder")
        assert response.status_code == 200
        data = response.json()
        
        # Verify schema layout
        assert "recommendation" in data
        assert "your_weakest_tags" in data
        assert "message" in data
        
        # Verify contents
        rec = data["recommendation"]
        assert rec["title"] == "Edit Distance"
        assert rec["difficulty"] == "Hard"
        assert rec["weakness_score"] == 0.98
        assert "dynamic-programming" in data["your_weakest_tags"]

def test_recommend_by_difficulty(test_client, mock_pipeline_result):
    """Test /recommend/{difficulty} endpoint filters correctly."""
    with patch("api.routes.run_pipeline", return_value=mock_pipeline_result):
        # Request Medium problems
        response = test_client.get("/recommend/medium?username=test_coder")
        assert response.status_code == 200
        data = response.json()
        
        rec = data["recommendation"]
        assert rec["title"] == "Longest Substring Without Repeating Characters"
        assert rec["difficulty"] == "Medium"
        assert rec["weakness_score"] == 0.85

def test_stats_endpoint(test_client, mock_pipeline_result):
    """Test /stats endpoint returns correct profile stats structures."""
    with patch("api.routes.run_pipeline", return_value=mock_pipeline_result):
        response = test_client.get("/stats?username=test_coder")
        assert response.status_code == 200
        data = response.json()
        
        assert data["username"] == "test_coder"
        assert data["solve_counts"]["All"] == 10
        assert len(data["tag_scores"]) == 3
        assert data["tag_scores"][0]["tag"] == "Dynamic Programming"

def test_update_endpoint(test_client, mock_pipeline_result):
    """Test /update POST endpoint purges local cache and fetches updates."""
    with patch("api.routes.run_pipeline", return_value=mock_pipeline_result):
        response = test_client.post("/update?username=test_coder")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "top_recommendation" in data
        assert data["top_recommendation"] == "Edit Distance"
