from fastapi import APIRouter
from app.services.generation_service import RagPipeline

router = APIRouter()
rag_pipeline = RagPipeline()

@router.post("/generate")
async def generate_response(company_name: str, talent: str, job: str, question: str, limit: str):
    answer = rag_pipeline.generate_answer(question, company_name, talent, job, limit)
    return {"answer": answer}
