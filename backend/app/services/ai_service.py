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

IMPORTANT QUALITY RULES:
- Do NOT use generic templates.
- Do NOT repeat the same topics.
- Tailor everything to the candidate's actual resume and the target job.
- Mention specific technologies from the resume and job description.
- Be concise, recruiter-friendly, and practical.
- Do not invent fake companies, fake projects, fake numbers, or fake experience.
- Prefer measurable impact only when the resume already supports it.
- Avoid long paragraphs.
- Avoid filler phrases.

OUTPUT LENGTH RULES:
- Resume bullets: maximum 22 words each.
- Interview questions: maximum 2 lines each.
- STAR answers: maximum 130 words each.
- Recruiter summary: maximum 4 sentences.

DIVERSITY RULES:
- Each resume bullet should focus on a different strength.
- Each interview question should test a different area.
- Each STAR answer must focus on a different theme:
  1. debugging or production issue
  2. deployment / automation / CI/CD
  3. architecture / scalability / system design

Return valid JSON only.
No markdown.
No explanations outside JSON.

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

RESUME BULLET RULES:
- Start with strong action verbs.
- Make each bullet ATS-friendly.
- Match the target job description.
- Include relevant technologies.
- Keep each bullet sharp and realistic.
- Do not overstuff keywords.

INTERVIEW QUESTION RULES:
- Ask questions specific to this resume and job description.
- Include technical, behavioral, architecture, debugging, and deployment questions.
- Avoid generic questions like "Tell me about yourself."
- Make questions realistic for software engineering interviews.

STAR ANSWER RULES:
- Use Situation, Task, Action, Result format.
- Make answers realistic for this candidate.
- Reference resume experience and target role needs.
- Keep each answer concise.
- Do not repeat the same story.

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

QUALITY RULES:
- Maximum 320 words.
- Professional but not robotic.
- Do not invent fake experience.
- Mention 2-3 strongest matching skills.
- Mention why the candidate fits the company or role.
- Use concise paragraphs.
- No markdown.
- No placeholders like [Company Name].
- Start directly with the letter.
- Avoid repeating the resume word-for-word.
- End with a confident, professional closing.

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