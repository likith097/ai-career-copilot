import os
import json
from google import genai


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception("Missing GEMINI_API_KEY")

    return genai.Client(api_key=api_key)


def _clean_json(text: str):
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    if text.startswith("```"):
        text = text.replace("```", "").strip()

    return json.loads(text)


def generate_ai_outputs(resume_text: str, job_description: str):
    client = get_client()

    prompt = f"""
You are an expert technical recruiter, resume coach, and software engineering interview coach.

Generate highly personalized outputs based ONLY on the resume and job description below.

Important:
- Do NOT use generic templates.
- Do NOT repeat the same interview questions for every user.
- Tailor everything to the candidate's actual projects, skills, experience, and the target job.
- Mention specific technologies from the resume and job description.
- Return valid JSON only.
- No markdown.
- No explanations outside JSON.

Return this exact JSON structure:

{{
  "ai_generated_bullets": [
    "bullet 1",
    "bullet 2",
    "bullet 3",
    "bullet 4",
    "bullet 5"
  ],
  "ai_interview_questions": [
    "question 1",
    "question 2",
    "question 3",
    "question 4",
    "question 5"
  ],
  "ai_star_answers": [
    "STAR answer 1",
    "STAR answer 2",
    "STAR answer 3"
  ],
  "ai_recruiter_summary": "3-4 sentence recruiter-style summary"
}}

Resume bullet rules:
- Strong action verbs
- ATS-friendly
- Tailored to the job description
- Mention relevant technologies
- Add measurable impact where possible
- Do not invent fake companies

Interview question rules:
- Ask questions specific to this resume and this job description
- Include technical, behavioral, architecture, and debugging questions
- Avoid generic questions like 'Tell me about yourself'

STAR answer rules:
- Use Situation, Task, Action, Result format
- Make answers realistic for this candidate
- Reference resume experience and target role needs

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text or "{}"

    try:
        data = _clean_json(text)
    except Exception:
        data = {
            "ai_generated_bullets": [],
            "ai_interview_questions": [],
            "ai_star_answers": [],
            "ai_recruiter_summary": ""
        }

    return {
        "ai_generated_bullets": data.get("ai_generated_bullets", [])[:5],
        "ai_interview_questions": data.get("ai_interview_questions", [])[:5],
        "ai_star_answers": data.get("ai_star_answers", [])[:3],
        "ai_recruiter_summary": data.get("ai_recruiter_summary", "")
    }


def generate_resume_bullets(resume_text: str, job_description: str):
    outputs = generate_ai_outputs(resume_text, job_description)
    return outputs["ai_generated_bullets"]

def generate_cover_letter(resume_text: str, job_description: str):
    client = get_client()

    prompt = f"""
You are an expert career coach and technical recruiter.

Write a personalized cover letter based ONLY on the resume and job description.

Rules:
- Maximum 350 words
- Professional but not robotic
- Do not invent fake experience
- Mention 2-3 strongest matching skills
- Mention why the candidate fits the company/role
- Use concise paragraphs
- No markdown
- No placeholders like [Company Name]
- Start directly with the letter

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return (response.text or "").strip()