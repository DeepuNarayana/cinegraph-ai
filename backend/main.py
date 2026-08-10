import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.recommendations import get_recommendations


app = FastAPI(
    title="CineGraph AI",
    description="AI-powered movie recommendation platform",
    version="1.0.0",
)


frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "CineGraph AI API is running"
    }


@app.get("/recommendations/{user_name}")
def recommendations(user_name: str):
    recommendations = get_recommendations(user_name)

    return {
        "user": user_name,
        "recommendations": recommendations,
    }