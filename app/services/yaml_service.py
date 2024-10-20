from docx import Document
import yaml
import os 

def split_paragraphs(file):
    """워드 파일을 단락별로 나누어 리스트로 반환"""
    doc = Document(file)
    contexts = [para.text for para in doc.paragraphs]
    contexts = "\n".join(contexts)
    paragraphs = contexts.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]

def process_word_to_yaml(file):
    """워드 파일을 처리하여 YAML 형식으로 변환"""
    paragraphs = split_paragraphs(file)
    
    yaml_content = {
        "에세이": {f"질문{i+1}": para for i, para in enumerate(paragraphs)}
    }

    return yaml_content

def save_yaml_content(filename: str, content: dict):
    """YAML 파일에 내용을 저장"""
    file_location = f"uploaded_files/{filename}"

    with open(file_location, "r", encoding="utf-8") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)

    # ['기업이름'], ['지원직무'], ['인재상'], ['지원시기'] 추가
    yaml_content["기업이름"] = content.get("기업이름", "")
    yaml_content["지원직무"] = content.get("지원직무", "")
    yaml_content["인재상"] = content.get("인재상", "")
    yaml_content["지원시기"] = content.get("지원시기", "")

    # ['에세이'] 내의 질문 내용 업데이트
    for key, value in content.items():
        if key.startswith("질문"):
            yaml_content["에세이"][key] = value

    with open(file_location, "w", encoding="utf-8") as yaml_file:
        yaml.dump(yaml_content, yaml_file, allow_unicode=True)

def load_yaml_content(filename: str):
    """YAML 파일에서 내용을 불러옴"""
    file_location = f"uploaded_files/{filename}"

    if not os.path.exists(file_location):
        return {"error": "File not found"}

    with open(file_location, "r", encoding="utf-8") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)

    return {
        "filename": filename,
        "content": {
            "기업이름": yaml_content.get("기업이름", ""),
            "지원직무": yaml_content.get("지원직무", ""),
            "인재상": yaml_content.get("인재상", ""),
            "지원시기": yaml_content.get("지원시기", ""),
            "에세이": yaml_content.get("에세이", {})
        }
    }
