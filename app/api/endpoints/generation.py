from fastapi import APIRouter
from app.services.generation_service import RagPipeline
from pydantic import BaseModel

class GenerationRequest(BaseModel):
    companyName: str
    talent: str
    job: str
    question: str
    limit: str
    context: str


def context_preprocess(inputs):

    total_contexts = ""

    split_contexts = inputs.split('AAA')

    for contexts in split_contexts:
        context = contexts.split('기업 이름:')

        relevant_part = context[0].strip()
 
        total_contexts += relevant_part + "\n\n"

    return  total_contexts

router = APIRouter()
rag_pipeline = RagPipeline()


@router.post("/generate")
async def generate_response(request: GenerationRequest):
    
    context = context_preprocess(request.context)
    
    answer = rag_pipeline.generate_answer(
        question=request.question,
        companyName=request.companyName,
        talent=request.talent,
        job=request.job,
        limit=request.limit,
        context=context
        )
    return {"answer": answer}
