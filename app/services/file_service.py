import os
import yaml
from fastapi import UploadFile
from app.services.yaml_service import process_word_to_yaml

upload_dir = "uploaded_files"

def save_file(file: UploadFile):
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # 파일 이름 중복 방지 처리
    yaml_filename = f"{upload_dir}/{file.filename.split('.')[0]}.yaml"
    base, ext = os.path.splitext(yaml_filename)
    counter = 1
    while os.path.exists(yaml_filename):
        yaml_filename = f"{base} ({counter}){ext}"
        counter += 1

    # 워드 파일을 YAML로 변환하여 저장
    yaml_content = process_word_to_yaml(file.file)

    # YAML 파일로 저장
    with open(yaml_filename, "w", encoding="utf-8") as yaml_file:
        yaml.dump(yaml_content, yaml_file, allow_unicode=True)

    return {"filename": os.path.basename(yaml_filename)}

def rename_file(old_filename: str, new_filename: str):
    old_file_path = os.path.join(upload_dir, old_filename)
    new_file_path = os.path.join(upload_dir, new_filename)

    if not os.path.exists(old_file_path):
        return {"error": "File not found"}

    # 파일명 중복 방지 처리
    base, ext = os.path.splitext(new_file_path)
    counter = 1
    while os.path.exists(new_file_path):
        new_file_path = f"{base} ({counter}){ext}"
        counter += 1

    os.rename(old_file_path, new_file_path)
    return {"message": "File renamed successfully"}

def delete_file(filename: str):
    file_path = os.path.join(upload_dir, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    os.remove(file_path)
    return {"message": "File deleted successfully"}

def get_uploaded_files():
    files = []
    if os.path.exists(upload_dir):
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                files.append({"filename": filename, "upload_time": os.path.getmtime(file_path)})
    return files
