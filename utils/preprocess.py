from docx import Document


def split_paragraphs(file):
    """워드 파일을 단락별로 나누어 리스트로 반환"""
    doc = Document(file)
    contexts = [para.text for para in doc.paragraphs]
    contexts = "\n".join(contexts)
    paragraphs = contexts.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]