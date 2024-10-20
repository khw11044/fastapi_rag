from fastapi import APIRouter, UploadFile, Form
from app.services import file_service, yaml_service

router = APIRouter()

# 파일 업로드 엔드포인트
@router.post("/upload")
async def upload_file(file: UploadFile):
    result = file_service.save_file(file)
    return result

# 업로드된 파일 목록 조회 엔드포인트
@router.get("/uploaded_files")
async def get_uploaded_files():
    return {"files": file_service.get_uploaded_files()}

# 파일 삭제 엔드포인트
@router.post("/delete")
async def delete_file(filename: str = Form(...)):
    result = file_service.delete_file(filename)
    return result

# 파일 이름 변경 엔드포인트
@router.post("/rename")
async def rename_file(old_filename: str = Form(...), new_filename: str = Form(...)):
    result = file_service.rename_file(old_filename, new_filename)
    return result

# 파일 내용 저장 엔드포인트
@router.post("/save")
async def save_file_content(data: dict):
    filename = data["filename"]
    content = data["content"]
    yaml_service.save_yaml_content(filename, content)
    return {"message": "File content saved successfully"}

# 파일 내용 조회 엔드포인트
@router.get("/{filename}")
async def get_file_content(filename: str):
    return yaml_service.load_yaml_content(filename)
