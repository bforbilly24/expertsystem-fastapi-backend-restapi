from fastapi import Query, HTTPException
from src.services.questions_service import get_paginated_questions, analyze_answers
from src.models.schemas import JawabanRequest, QuestionsResponse, StatusResponse, AnalysisResponse

async def get_questions(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=50)):
    try:
        return QuestionsResponse(**get_paginated_questions(page, per_page))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching questions: {str(e)}")

async def analyze(data: JawabanRequest):
    try:
        return AnalysisResponse(**analyze_answers(data.jawaban))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")

async def get_status():
    return StatusResponse(message="success")