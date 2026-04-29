from app.services.ai_service import generate_resume_bullets
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.parser import extract_text_from_pdf
from app.services.llm import analyze_with_ai

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "AI Career Copilot"}


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

    ai_generated_bullets = generate_resume_bullets(
        payload.resume_text,
        payload.job_description
    )

    result["ai_generated_bullets"] = ai_generated_bullets

    return result