from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import shutil
import os
from pathlib import Path
from docx import Document
from datetime import datetime
import yaml

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


def split_paragraphs(file):
    """워드 파일을 단락별로 나누어 리스트로 반환"""
    doc = Document(file)
    contexts = [para.text for para in doc.paragraphs]
    contexts = "\n".join(contexts)
    paragraphs = contexts.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]


# 루트 페이지
@app.get("/")
async def root():
    return FileResponse('static/index.html')


# '내 자소서 쓰기' 페이지
@app.get("/write")
async def write_page():
    return FileResponse('static/write.html')


@app.on_event("startup")
async def load_existing_files():
    upload_dir = "uploaded_files"

    # 폴더가 존재하면 파일 목록을 가져와서 업데이트
    if os.path.exists(upload_dir):
        uploaded_files_info.clear()  # 기존 목록을 초기화
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                uploaded_files_info.append({
                    "filename": filename,
                    "upload_time": upload_time
                })


@app.post("/delete_file")
async def delete_file(filename: str = Form(...)):
    upload_dir = "uploaded_files"
    file_path = os.path.join(upload_dir, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    try:
        os.remove(file_path)
    except Exception as e:
        return {"error": f"Failed to delete file: {str(e)}"}

    uploaded_files_info[:] = [file for file in uploaded_files_info if file["filename"] != filename]
    return {"message": "File deleted successfully"}


@app.post("/process_word")
async def process_word_file(file: UploadFile = File(...)):
    upload_dir = "uploaded_files"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    if not file.filename.endswith((".docx", ".doc")):
        return {"error": "Invalid file type. Please upload a .docx or .doc file."}

    yaml_filename = f"{upload_dir}/{file.filename.split('.')[0]}.yaml"
    base, ext = os.path.splitext(yaml_filename)
    counter = 1

    while os.path.exists(yaml_filename):
        yaml_filename = f"{base} ({counter}){ext}"
        counter += 1

    paragraphs = split_paragraphs(file.file)
    yaml_content = {
        "에세이": {f"질문{i+1}": para for i, para in enumerate(paragraphs)}
    }

    with open(yaml_filename, "w", encoding="utf-8") as yaml_file:
        yaml.dump(yaml_content, yaml_file, allow_unicode=True)

    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uploaded_files_info.append({
        "filename": os.path.basename(yaml_filename),
        "upload_time": upload_time
    })

    return {"filename": os.path.basename(yaml_filename), "content": yaml_content}


@app.get("/uploaded_files")
async def get_uploaded_files():
    return {"files": uploaded_files_info}


@app.post("/rename_file")
async def rename_file(old_filename: str = Form(...), new_filename: str = Form(...)):
    upload_dir = "uploaded_files"
    old_file_path = os.path.join(upload_dir, old_filename)
    new_file_path = os.path.join(upload_dir, new_filename)

    if not os.path.exists(old_file_path):
        return {"error": "File not found"}

    base, ext = os.path.splitext(new_file_path)
    counter = 1
    while os.path.exists(new_file_path):
        new_file_path = f"{base} ({counter}){ext}"
        counter += 1

    os.rename(old_file_path, new_file_path)

    for file_info in uploaded_files_info:
        if file_info["filename"] == old_filename:
            file_info["filename"] = os.path.basename(new_file_path)

    return {"message": "File renamed successfully", "new_filename": os.path.basename(new_file_path)}


@app.post("/save_file_content")
async def save_file_content(data: dict):
    filename = data["filename"]
    content = data["content"]

    file_location = f"uploaded_files/{filename}"

    if not os.path.exists(file_location):
        return {"error": "File not found"}

    with open(file_location, "r", encoding="utf-8") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)

    # ['기업이름']과 ['지원직무'] 추가
    yaml_content["기업이름"] = content.get("기업이름", "")
    yaml_content["지원직무"] = content.get("지원직무", "")

    # ['에세이'] 내의 질문 내용 업데이트
    for key, value in content.items():
        if key.startswith("질문"):
            yaml_content["에세이"][key] = value

    with open(file_location, "w", encoding="utf-8") as yaml_file:
        yaml.dump(yaml_content, yaml_file, allow_unicode=True)

    return {"message": "File content saved successfully"}


@app.get("/file_content/{filename}")
async def get_file_content(filename: str):
    file_location = f"uploaded_files/{filename}"

    if not os.path.exists(file_location):
        return {"error": "File not found"}

    with open(file_location, "r", encoding="utf-8") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)

    return {
        "filename": filename,
        "content": {
            "기업이름": yaml_content.get("기업이름", ""),  # 기업이름 반환
            "지원직무": yaml_content.get("지원직무", ""),  # 지원직무 반환
            "에세이": yaml_content.get("에세이", {})  # 에세이 내용 반환
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
