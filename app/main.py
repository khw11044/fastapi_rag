# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import files

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

# 루트 경로에 index.html 반환
@app.get("/")
async def root():
    return FileResponse('static/index.html')

from fastapi.responses import FileResponse

# '내 자소서 쓰기' 페이지 라우트
@app.get("/write")
async def write_page():
    return FileResponse('static/write.html')


# 파일 관련 라우터 등록
app.include_router(files.router, prefix="/files", tags=["files"])