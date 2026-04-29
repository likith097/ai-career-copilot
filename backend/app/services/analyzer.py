import re
from collections import Counter
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KEYWORD_CATEGORIES: Dict[str, List[str]] = {
    "Languages": ["python", "typescript", "javascript", "java", "c++", "c#", "sql", "bash"],
    "Backend": ["fastapi", "node", "node.js", "express", "nestjs", "rest api", "api", "microservices", "backend", "distributed systems"],
    "Frontend": ["react", "next.js", "angular", "tailwind", "html", "css", "frontend", "ui"],
    "Data & AI": ["machine learning", "ml", "ai", "nlp", "rag", "llm", "embeddings", "vector", "computer vision", "opencv", "tensorflow", "pytorch", "scikit-learn"],
    "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "linux", "git", "github actions", "ci/cd", "devops", "cloud", "deployment"],
    "Databases": ["postgresql", "mysql", "mongodb", "nosql", "oracle", "sql server", "redis", "database", "databases"],
    "Testing & Quality": ["testing", "pytest", "unit testing", "integration testing", "automated testing", "monitoring", "logging", "observability"],
    "Engineering Signals": ["agile", "scrum", "ownership", "scalable", "reliability", "performance", "automation", "debugging", "production", "collaboration"],
}

ACTION_VERBS = [
    "engineered", "built", "deployed", "optimized", "automated", "integrated", "scaled", "designed", "implemented", "improved", "reduced", "delivered"
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def contains_term(text: str, term: str) -> bool:
    pattern = r"(?<![a-z0-9+#.])" + re.escape(term.lower()) + r"(?![a-z0-9+#.])"
    return bool(re.search(pattern, text.lower()))


def extract_jd_keywords(job_description: str) -> List[str]:
    jd = normalize(job_description)
    found = []
    for terms in KEYWORD_CATEGORIES.values():
        for term in terms:
            if contains_term(jd, term) and term not in found:
                found.append(term)
    return found


def keyword_gap(resume_text: str, job_description: str) -> Tuple[List[str], List[str]]:
    resume = normalize(resume_text)
    jd_keywords = extract_jd_keywords(job_description)
    matched = [kw for kw in jd_keywords if contains_term(resume, kw)]
    missing = [kw for kw in jd_keywords if kw not in matched]
    return matched, missing


def category_coverage(resume_text: str, job_description: str) -> Dict[str, Dict[str, List[str] | int]]:
    resume = normalize(resume_text)
    jd = normalize(job_description)
    coverage = {}
    for category, terms in KEYWORD_CATEGORIES.items():
        jd_terms = [t for t in terms if contains_term(jd, t)]
        matched = [t for t in jd_terms if contains_term(resume, t)]
        missing = [t for t in jd_terms if t not in matched]
        if jd_terms:
            coverage[category] = {
                "matched": matched,
                "missing": missing,
                "score": int((len(matched) / max(1, len(jd_terms))) * 100),
            }
    return coverage


def metric_strength(resume_text: str) -> int:
    text = resume_text.lower()
    numbers = re.findall(r"\b\d+(?:\.\d+)?\s?(?:%|x|k|m|tb|gb|ms|seconds?|minutes?|hours?|users?|requests?|frames?|models?|apis?)?\b", text)
    action_count = sum(text.count(v) for v in ACTION_VERBS)
    score = min(100, len(numbers) * 7 + action_count * 6)
    return score


def section_strength(resume_text: str) -> int:
    text = resume_text.lower()
    sections = ["summary", "technical skills", "skills", "experience", "projects", "education", "certifications"]
    return int((sum(1 for s in sections if s in text) / len(sections)) * 100)


def ats_score(resume_text: str, job_description: str) -> int:
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=3500)
    matrix = vectorizer.fit_transform([resume_text, job_description])
    semantic = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    matched, missing = keyword_gap(resume_text, job_description)
    keyword = len(matched) / max(1, len(matched) + len(missing))
    impact = metric_strength(resume_text) / 100
    sections = section_strength(resume_text) / 100
    score = int((0.42 * semantic + 0.38 * keyword + 0.12 * impact + 0.08 * sections) * 100)
    return max(5, min(score, 98))


def top_terms(text: str, limit: int = 10) -> List[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z+#.]{2,}", normalize(text))
    stop = {"and", "the", "for", "with", "that", "this", "from", "you", "our", "your", "are", "will", "using", "work", "role", "team", "software"}
    counts = Counter(w for w in words if w not in stop)
    return [w for w, _ in counts.most_common(limit)]


def generate_rule_based_outputs(resume_text: str, job_description: str) -> dict:
    matched, missing = keyword_gap(resume_text, job_description)
    score = ats_score(resume_text, job_description)
    categories = category_coverage(resume_text, job_description)
    jd_terms = top_terms(job_description, 12)

    focus_terms = ", ".join(matched[:8]) if matched else "software engineering, APIs, production systems"
    missing_terms = ", ".join(missing[:8]) if missing else "no major keyword gaps"
    strongest_categories = [name for name, data in categories.items() if int(data["score"]) >= 60]
    weak_categories = [name for name, data in categories.items() if int(data["score"]) < 60]

    improved_bullets = [
        f"Engineered production-ready systems across {focus_terms}, translating business requirements into scalable APIs, reliable services, and measurable delivery outcomes.",
        "Built and deployed full-stack features with clean REST API contracts, reusable frontend components, and automated validation workflows to improve release quality.",
        "Optimized resume-to-job matching using TF-IDF semantic similarity, weighted keyword coverage, section completeness checks, and explainable scoring logic.",
        f"Strengthened role alignment by adding targeted evidence for {missing_terms} through projects, quantified achievements, and recruiter-facing technical keywords.",
    ]

    action_plan = [
        f"Add 2-3 resume bullets explicitly mentioning: {missing_terms}.",
        "Add metrics to every major project or job bullet: latency, accuracy, users, volume, cost, deployment time, or reliability.",
        "Add a Projects section with this app: React, TypeScript, FastAPI, Python, REST APIs, TF-IDF scoring, PDF parsing, and deployment.",
        "Push to GitHub with screenshots, setup instructions, architecture diagram, and a live demo link.",
    ]

    questions = [
        "Walk me through the architecture of your AI Career Copilot project.",
        "How does your ATS scoring logic combine semantic similarity and keyword matching?",
        "How would you improve reliability if LLM-generated suggestions were added?",
        "How would you deploy this application for real users with authentication and saved reports?",
        "Describe a production issue you debugged and how you found the root cause.",
        "How would you test resume parsing, scoring quality, and frontend/backend integration?",
    ]

    star_answers = [
        "Situation: Job seekers often struggle to understand why a resume does not match a role. Task: Build a practical AI-enabled tool that compares resumes with job descriptions. Action: Implemented a React/TypeScript frontend, FastAPI backend, PDF parsing, TF-IDF similarity, keyword gap extraction, and structured interview prep outputs. Result: Delivered a full-stack portfolio project that demonstrates API design, text processing, product thinking, and deployment-ready engineering.",
        "Situation: The first scoring version produced shallow keyword-only output. Task: Make the system more recruiter-relevant. Action: Added weighted scoring across semantic similarity, keyword coverage, section completeness, and quantified-impact signals. Result: Produced more explainable recommendations and a stronger project story for software engineering and AI engineering interviews.",
    ]

    summary = (
        f"Estimated ATS alignment: {score}/100. Strongest match areas: "
        f"{', '.join(strongest_categories[:4]) if strongest_categories else focus_terms}. "
        f"Primary improvement areas: {', '.join(weak_categories[:4]) if weak_categories else missing_terms}. "
        f"Top JD signals detected: {', '.join(jd_terms[:8])}."
    )

    return {
        "ats_score": score,
        "summary": summary,
        "keyword_gap": {"matched_keywords": matched, "missing_keywords": missing},
        "category_coverage": categories,
        "improved_bullets": improved_bullets,
        "interview_questions": questions,
        "star_answers": star_answers,
        "action_plan": action_plan,
        "resume_quality": {
            "metric_strength": metric_strength(resume_text),
            "section_strength": section_strength(resume_text),
            "jd_terms_detected": jd_terms,
        },
    }
