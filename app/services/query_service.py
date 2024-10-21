import os
import glob
import yaml
from langchain_core.documents import Document
from langchain_teddynote.retrievers import KiwiBM25Retriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever

def get_info_yaml(path):
    with open(path, encoding='utf-8') as f:  # UTF-8 인코딩 명시
        file = yaml.full_load(f)

    metadata_company = file.get('기업이름', '')
    metadata_day = file.get('지원시기', '')
    metadata_job = file.get('지원직무', '')
    metadata_talentedperson = file.get('인재상', '')

    Documents = []
    for key, value in file['에세이'].items():
        doc = Document(value)
        doc.metadata["기업이름"] = metadata_company
        doc.metadata["지원시기"] = metadata_day
        doc.metadata["지원직무"] = metadata_job
        doc.metadata["인재상"] = metadata_talentedperson
        doc.metadata["question"] = value.split('\n')[0]
        Documents.append(doc)
    
    return Documents

def process_query(query: str):
    files = glob.glob('./uploaded_files/*')
    all_Docs = []
    for file in files:
        docs = get_info_yaml(file)
        all_Docs.extend(docs)

    kiwi_bm25_retriever = KiwiBM25Retriever.from_documents(all_Docs)
    answers = kiwi_bm25_retriever.invoke(query)
    # reranker = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")
    # compressor = CrossEncoderReranker(model=reranker, top_n=5)
    
    # compression_retriever = ContextualCompressionRetriever(
    #         base_compressor=compressor, base_retriever=kiwi_bm25_retriever)
    
    # answers = compression_retriever.invoke(query)
    
    # 결과를 출력 형태로 변환
    results = []
    for ans in answers:

        texts = ans.page_content
        lines = texts.splitlines()
        results.append({
            "content": "\n".join(lines[1:]),
            "metadata": ans.metadata
        })
    return results
