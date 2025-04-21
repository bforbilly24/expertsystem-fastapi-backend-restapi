from pydantic import BaseModel, Field
from typing import List

class JawabanRequest(BaseModel):
    jawaban: List[int] = Field(..., min_items=50, max_items=50)

class QuestionsResponse(BaseModel):
    soal: List[str]
    page: int
    per_page: int
    total_questions: int
    total_pages: int

class StatusResponse(BaseModel):
    message: str

class AnalysisResponse(BaseModel):
    hasil: str