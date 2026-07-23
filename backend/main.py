from fastapi import FastAPI
from pydantic import BaseModel

from backend.services.gap_engine import GapEngine

app = FastAPI(
    title="ResearchRadar API",
    description="AI-Powered Research Gap Discovery Engine",
    version="1.0.0"
)

engine = GapEngine()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {
        "message": "ResearchRadar API is running!"
    }


@app.post("/analyze")
def analyze(request: QueryRequest):

    result = engine.analyze(request.query)

    return result