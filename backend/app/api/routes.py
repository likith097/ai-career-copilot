from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.parser import extract_text_from_pdf
from app.services.llm import analyze_with_ai

try:
    from app.services.ai_service import generate_resume_bullets
except Exception:
    generate_resume_bullets = None

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "AI Career Copilot"}


@router.get("/test-gemini")
def test_gemini():
    if not generate_resume_bullets:
        return {
            "gemini_working": False,
            "error": "Gemini service import failed"
        }

    try:
        bullets = generate_resume_bullets(
            resume_text="Software engineer with React, Python, FastAPI, AWS, SQL and Docker experience.",
            job_description="Hiring a full-stack engineer with React, Python, APIs, cloud and databases."
        )

        return {
            "gemini_working": True,
            "sample_output": bullets
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

    if generate_resume_bullets:
        try:
            bullets = generate_resume_bullets(
                payload.resume_text,
                payload.job_description
            )
            result["ai_generated_bullets"] = bullets
        except Exception as e:
            print(f"Gemini generation failed: {e}")

    return result