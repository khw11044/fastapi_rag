from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
import shutil
import os
from pathlib import Path
from docx import Document
from datetime import datetime

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

# 업로드된 파일 정보 저장을 위한 리스트
uploaded_files_info = []

# 루트 페이지
@app.get("/")
async def root():
    return FileResponse('static/index.html')

# 워드 파일 업로드 및 처리
@app.post("/process_word")
async def process_word_file(file: UploadFile = File(...)):
    # 업로드된 파일을 저장할 폴더 경로
    upload_dir = "uploaded_files"
    
    # 디렉터리가 없으면 생성
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # 파일 확장자 확인
    if not file.filename.endswith((".docx", ".doc")):
        return {"error": "Invalid file type. Please upload a .docx or .doc file."}

    # 업로드한 파일을 임시로 저장
    file_location = f"{upload_dir}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 파일 이름과 업로드 날짜 기록
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uploaded_files_info.append({
        "filename": file.filename,
        "upload_time": upload_time
    })

    # 워드 파일 내용 읽기
    doc = Document(file_location)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    # 워드 파일 내용을 반환
    return {"filename": file.filename, "content": "\n".join(full_text)}

# 업로드된 파일 목록 제공 API
@app.get("/uploaded_files")
async def get_uploaded_files():
    return {"files": uploaded_files_info}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
