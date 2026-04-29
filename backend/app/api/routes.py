from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.parser import extract_text_from_pdf
from app.services.llm import analyze_with_ai

try:
    from app.services.ai_service import generate_ai_outputs
except Exception:
    generate_ai_outputs = None

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "AI Career Copilot"}


@router.get("/test-gemini")
def test_gemini():
    if not generate_ai_outputs:
        return {
            "gemini_working": False,
            "error": "Gemini service import failed"
        }

    try:
        outputs = generate_ai_outputs(
            resume_text="Software engineer with React, Python, FastAPI, AWS, SQL and Docker experience.",
            job_description="Hiring a full-stack engineer with React, Python, APIs, cloud and databases."
        )

        return {
            "gemini_working": True,
            "sample_output": outputs
        }

    except Exception as e:
        return {
            "gemini_working": False,
            "error": str(e)
        }


@router.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF resume.")

    content = await file.read()
    text = extract_text_from_pdf(content)

    if not text:
        raise HTTPException(status_code=422, detail="Could not extract text from PDF.")

    return {"filename": file.filename, "text": text}


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(payload: AnalyzeRequest):
    result = await analyze_with_ai(
        payload.resume_text,
        payload.job_description
    )

    result["ai_generated_bullets"] = []
    result["ai_interview_questions"] = []
    result["ai_star_answers"] = []
    result["ai_recruiter_summary"] = ""

    if generate_ai_outputs:
        try:
            ai_outputs = generate_ai_outputs(
                payload.resume_text,
                payload.job_description
            )

            result["ai_generated_bullets"] = ai_outputs.get("ai_generated_bullets", [])
            result["ai_interview_questions"] = ai_outputs.get("ai_interview_questions", [])
            result["ai_star_answers"] = ai_outputs.get("ai_star_answers", [])
            result["ai_recruiter_summary"] = ai_outputs.get("ai_recruiter_summary", "")

        except Exception as e:
            print(f"Gemini generation failed: {e}")

    return result