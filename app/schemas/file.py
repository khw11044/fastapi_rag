# app/schemas/file.py
from pydantic import BaseModel
from typing import Dict

class FileBase(BaseModel):
    filename: str

class FileCreate(FileBase):
    content: Dict[str, str]  # YAML 파일에 저장될 'content'는 딕셔너리 형태로 받습니다.

class FileResponse(FileBase):
    upload_time: str  # 파일 업로드 시각 포함
    content: Dict[str, str]  # 응답으로 돌려줄 파일의 내용

class FileContentUpdate(BaseModel):
    filename: str
    content: Dict[str, str]  # 수정할 내용은 딕셔너리 형태로 받음
