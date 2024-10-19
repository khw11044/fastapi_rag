
# Langchain Rag FastAPI

## Section 3.1 주어진 워드파일들로 Documents 만들기 or DB화 하기 


![image](https://github.com/user-attachments/assets/f0cc199e-7dcf-437c-9c29-9e8aed3689dd)

일단 현재까지 한것


Sparse를 하든 Dense를 하든 DB화 하기 

이후에 '내 자소서 쓰기'에서 RAG가 내가 준비한 자소서 기반으로 

요청한 에세이 질문에 답변하기 위해 


+ 이후에 할거 

질문 쿼리 입력 박스랑 

구체적인 규칙 요청 프롬프트 입력 박스도 만들자. 

예) 

- 기업의 인재상 넣기 
- 나의 구체적인 어떤 경험 또는 역량을 강조해서 작성해달라고 하기 

현재는 자소서만 입력받지만 나중에는 내 이력서도 받을 수 있게 하자.


> pip install -r requirements.txt 

> uvicorn main:app --reload