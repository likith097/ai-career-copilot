import os
from google import genai


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("Missing GEMINI_API_KEY")

    return genai.Client(api_key=api_key)


def generate_resume_bullets(resume_text: str, job_description: str):
    client = get_client()

    prompt = f"""
You are an expert resume writer.

Rewrite 5 powerful ATS-friendly resume bullet points based on this candidate resume and job description.

Rules:
- Strong action verbs
- Quantify impact where possible
- Relevant to target role
- Short and professional
- Return only bullet points

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text or ""

    bullets = []
    for line in text.splitlines():
        clean = line.strip("-•1234567890. ").strip()
        if clean:
            bullets.append(clean)

    return bullets[:5]