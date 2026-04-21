from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class ProblemRecommendation(BaseModel):
    title: str
    titleSlug: str
    difficulty: str
    acceptance_rate: float
    tags: List[str]
    weakness_score: float
    leetcode_url: str


class RecommendationResponse(BaseModel):
    recommendation: ProblemRecommendation
    your_weakest_tags: List[str]
    message: str


class UpdateResponse(BaseModel):
    success: bool
    message: str
    top_recommendation: Optional[str] = None


class TagScore(BaseModel):
    tag: str
    solved: int
    strength_score: float
    weakness_score: float


class UserStatsResponse(BaseModel):
    username: str
    solve_counts: Dict[str, Any]
    total_available: Dict[str, Any]
    tag_scores: List[TagScore]