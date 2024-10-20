from fastapi import APIRouter
from pydantic import BaseModel
from app.services.query_service import process_query  # 검색 로직을 서비스로 분리

router = APIRouter()

# QueryInput 모델 정의
class QueryInput(BaseModel):
    query: str

# /query 엔드포인트 생성
@router.post("/query")
async def query(query_input: QueryInput):
    results = process_query(query_input.query)  # 서비스 함수 호출
    return {"results": results}
