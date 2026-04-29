# AI Career Copilot

A 6-hour portfolio project that demonstrates full-stack software engineering and AI engineering fundamentals.

## What it does

Users can upload a resume PDF or paste resume text, paste a job description, and generate:

- ATS match score
- Matched keywords
- Missing keywords
- Improved resume bullets
- Interview questions
- STAR-format answers

## Tech Stack

- Frontend: React, TypeScript, Vite, CSS
- Backend: Python, FastAPI, Pydantic
- AI/ML: TF-IDF similarity, keyword extraction, rule-based AI fallback
- Parsing: PDF text extraction with pypdf
- DevOps: Docker, Docker Compose, GitHub Actions
- Testing: Pytest

## Why this project is strong for resumes

It shows practical skills across:

- REST API design
- Frontend engineering
- Backend engineering
- AI workflow design
- Resume/JD parsing
- ATS-style scoring
- Prompt-ready architecture
- Testing
- Dockerized deployment
- CI/CD pipeline

## Run in VS Code without Docker

### 1. Open project

Open the `ai-career-copilot` folder in VS Code.

### 2. Start backend

```bash
cd backend
python -m venv .venv
```

Activate environment:

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

### 3. Start frontend

Open a second VS Code terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## Run with Docker

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

## Test backend

```bash
cd backend
pytest
```

## Suggested GitHub repo description

Full-stack AI career platform using FastAPI, React, TypeScript, PDF parsing, ATS scoring, keyword extraction, Docker, and CI/CD to analyze resumes against job descriptions and generate interview preparation workflows.

## Resume bullet

Engineered an AI-powered career optimization platform using FastAPI, React, TypeScript, PDF parsing, and ATS-style NLP scoring to analyze resumes against job descriptions, identify keyword gaps, generate improved resume bullets, and create personalized interview preparation workflows.

## Future improvements

- Add PostgreSQL for saved analyses
- Add user authentication
- Add OpenAI or Claude API integration
- Add real embeddings with ChromaDB or FAISS
- Add downloadable PDF report
- Deploy backend to Render and frontend to Vercel
