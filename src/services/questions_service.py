import joblib
import pandas as pd
import numpy as np
from math import ceil
from fastapi import HTTPException

# File paths
MODEL_PATH = "src/ml_model/mlp_model.pkl"
FILE_PATH_SOAL = "src/data/pertanyaan.csv"

# Load model
try:
    loaded_model = joblib.load(MODEL_PATH)
except Exception as e:
    raise Exception(f"Failed to load model: {str(e)}")

# Load questions
try:
    df = pd.read_csv(FILE_PATH_SOAL)
    soal_list = df["Soal"].tolist()
    # Ensure exactly 50 questions
    if len(soal_list) < 50:
        raise Exception(f"Expected at least 50 questions, got {len(soal_list)}")
    soal_list = soal_list[:50]  # Take only the first 50 questions
except Exception as e:
    raise Exception(f"Failed to load questions: {str(e)}")

# ID to label mapping
id2label = {
    0: 'Backend Developer',
    1: 'Data Scientist',
    2: 'Frontend Developer',
    3: 'Product Manager',
    4: 'UI/UX Designer'
}

# Number of questions
JUMLAH_SOAL = 50  # Fixed to 50

def get_paginated_questions(page: int, per_page: int):
    total_questions = JUMLAH_SOAL
    total_pages = ceil(total_questions / per_page)

    if not soal_list:
        raise HTTPException(status_code=500, detail="No questions available.")
    if page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid page number. Must be between 1 and {total_pages}."
        )

    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_questions)
    paginated_questions = soal_list[start_idx:end_idx]

    print(f"get_paginated_questions: page={page}, per_page={per_page}, start_idx={start_idx}, end_idx={end_idx}, questions={len(paginated_questions)}")
    return {
        "soal": paginated_questions,
        "page": page,
        "per_page": per_page,
        "total_questions": total_questions,
        "total_pages": total_pages
    }

def analyze_answers(jawaban: list[int]):
    if not jawaban or len(jawaban) != JUMLAH_SOAL:
        raise HTTPException(
            status_code=400,
            detail=f"Jawaban tidak lengkap atau tidak valid. Expected {JUMLAH_SOAL} answers, got {len(jawaban)}."
        )
    if any(x < 1 or x > 5 for x in jawaban):
        raise HTTPException(
            status_code=400,
            detail="All answers must be integers between 1 and 5."
        )

    jawaban_2d = np.array(jawaban).reshape(1, -1)
    pred = loaded_model.predict(jawaban_2d)
    label_prediksi = id2label[pred[0]]

    print(f"analyze_answers: Received {len(jawaban)} answers, predicted: {label_prediksi}")
    return {"hasil": label_prediksi}