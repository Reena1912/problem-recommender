from unittest.mock import patch
import pytest
from api.user_pipeline import run_pipeline, _cache

def test_run_pipeline_success(mock_problems_catalog, mock_user_profile_data, mock_solved_slugs):
    """Test full user analysis pipeline runs and correctly ranks unsolved problems."""
    # Clear cache to guarantee run
    _cache.clear()

    with patch("api.user_pipeline.fetch_user_profile_data", return_value=mock_user_profile_data) as mock_fetch_profile, \
         patch("api.user_pipeline.fetch_solved_slugs_data", return_value=mock_solved_slugs) as mock_fetch_solved:
        
        username = "test_coder"
        result = run_pipeline(username, mock_problems_catalog, "session_123")

        # Verify profile queries were invoked
        mock_fetch_profile.assert_called_once_with(username, "session_123")
        mock_fetch_solved.assert_called_once_with(username, "session_123")

        # Verify schema layout
        assert "ranked_problems" in result
        assert "weakness_map" in result
        assert "tag_scores" in result
        assert "solve_counts" in result
        assert "total_available" in result

        # Verify solved problems are filtered out
        ranked_slugs = [p["titleSlug"] for p in result["ranked_problems"]]
        assert "two-sum" not in ranked_slugs  # two-sum is solved, must be omitted

        # Verify ranking priorities
        # 'Edit Distance' targets Dynamic Programming (0 solved, high weakness)
        # 'Longest Substring' targets Sliding Window / Hash Table (0 solved)
        # Median of Two Sorted Arrays targets Array (1 solved, lower weakness)
        # Therefore, Edit Distance should have a higher weakness score than Median of Two Sorted Arrays
        edit_dist = next(p for p in result["ranked_problems"] if p["titleSlug"] == "edit-distance")
        median_two = next(p for p in result["ranked_problems"] if p["titleSlug"] == "median-of-two-sorted-arrays")

        assert edit_dist["weakness_score"] >= median_two["weakness_score"]
        # The problems list should be sorted by weakness score descending
        scores = [p["weakness_score"] for p in result["ranked_problems"]]
        assert scores == sorted(scores, reverse=True)

def test_run_pipeline_user_not_found():
    """Test pipeline throws ValueError when the username doesn't exist on LeetCode."""
    _cache.clear()
    empty_profile = {"data": {"matchedUser": None}}

    with patch("api.user_pipeline.fetch_user_profile_data", return_value=empty_profile):
        with pytest.raises(ValueError, match="LeetCode user 'non_existent_user' not found."):
            run_pipeline("non_existent_user", [], "session_123")
