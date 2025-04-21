from fastapi import APIRouter
from src.controllers.questions_controller import get_questions, analyze, get_status

router = APIRouter(prefix="/api/v1")

router.get("/questions")(get_questions)
router.post("/analysis")(analyze)
router.get("/status")(get_status)