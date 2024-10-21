from fastapi import APIRouter
from app.services.generation_service import RagPipeline
from pydantic import BaseModel

class GenerationRequest(BaseModel):
    companyName: str
    talent: str
    job: str
    question: str
    limit: str
    
router = APIRouter()
rag_pipeline = RagPipeline()



@router.post("/generate")
async def generate_response(request: GenerationRequest):
    answer = rag_pipeline.generate_answer(
        question=request.question,
        companyName=request.companyName,
        talent=request.talent,
        job=request.job,
        limit=request.limit
        )
    return {"answer": answer}
