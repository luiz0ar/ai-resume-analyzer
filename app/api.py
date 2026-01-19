from fastapi import FastAPI, HTTPException
from app.config import get_settings
from app.models import ResumeInput, ResumeScore
from app.services import AIService, AIServiceError
from app.utils import read_prompt_file

app = FastAPI(title="AI Resume Analyzer", version="1.0.0")

settings = get_settings()
system_prompt = read_prompt_file(settings.scoring_prompt_path)

ai_service = AIService(
    api_key=settings.openai_api_key,
    model=settings.openai_model,
    temperature=settings.openai_temperature,
    max_tokens=settings.openai_max_tokens,
)


@app.get("/health", summary="Health Check", tags=["System"])
async def health_check():
    if await ai_service.health_check():
        return {"status": "ok"}
    raise HTTPException(status_code=503, detail="OpenAI API is unavailable")


@app.post("/analyze", response_model=ResumeScore, summary="Analyze Resume", tags=["Analysis"])
async def analyze_resume(input_data: ResumeInput):
    try:
        result = await ai_service.analyze_resume(
            resume_input=input_data,
            system_prompt=system_prompt,
        )
        return result
    except AIServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))