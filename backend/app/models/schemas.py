from pydantic import BaseModel, Field
from typing import Dict, List, Union


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=20)
    job_description: str = Field(..., min_length=20)


class KeywordGap(BaseModel):
    matched_keywords: List[str]
    missing_keywords: List[str]


class CategoryCoverage(BaseModel):
    matched: List[str]
    missing: List[str]
    score: int


class ResumeQuality(BaseModel):
    metric_strength: int
    section_strength: int
    jd_terms_detected: List[str]


class AnalyzeResponse(BaseModel):
    ats_score: int
    summary: str
    keyword_gap: KeywordGap
    category_coverage: Dict[str, CategoryCoverage] = {}
    improved_bullets: List[str]
    interview_questions: List[str]
    star_answers: List[str]
    action_plan: List[str] = []
    resume_quality: ResumeQuality | None = None
