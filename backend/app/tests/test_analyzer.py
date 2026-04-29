from app.services.analyzer import ats_score, keyword_gap


def test_ats_score_range():
    score = ats_score("Python FastAPI Docker AWS", "Python Docker backend API")
    assert 1 <= score <= 99


def test_keyword_gap():
    matched, missing = keyword_gap("Python Docker", "Need Python Docker Kubernetes")
    assert "python" in matched
    assert "docker" in matched
    assert "kubernetes" in missing
