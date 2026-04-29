from app.core.config import settings
from app.services.analyzer import generate_rule_based_outputs


async def analyze_with_ai(resume_text: str, job_description: str) -> dict:
    """Mock-first AI layer.

    This project runs without paid API keys. For production, replace this with an
    OpenAI/Claude call and keep the same response schema.
    """
    # Safe default for portfolio demos and local coding sessions.
    return generate_rule_based_outputs(resume_text, job_description)
