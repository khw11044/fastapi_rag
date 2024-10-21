from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()

class RagPipeline:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.1)
        self.chain = self.init_chain()

    def init_chain(self):
        template = """
        당신은 자기소개서 작성 도우미입니다. 
        당신은 나에 대해서 굉장히 잘 알고 있습니다.
        나는 '지원 기업'에 입사하기 위해 자기소개서를 작성하고 있습니다.
        '내가 이전에 작성했던 자소서'와 '기업 인재상' 및 '지원 직무'를 참고하여 기업의 질문에 대한 적절한 답변을 작성해주세요.

        작성 내용의 구조는 아래와 같은 규칙으로 작성해주세요.
        1. 질문에 대한 두괄식으로 작성해주세요.
        2. 나의 경험과 역량 그리고 기업과 직무를 고려하여 작성해주세요.
        3. 답변은 반드시 글자수 {limit} 미만으로 작성해주세요.
        4. 내가 현재 어느 기업에 지원하고 있는지 '지원 기업'을 잊지마세요.

        # 지원 기업:
        {company}
        
        # 기업 인재상:
        {talent}
        
        # 지원 직무:
        {job}
        
        # 내가 이전에 작성했던 자소서:
        {context}

        # 질문:
        {question}

        ### 답변:
        """

        prompt = PromptTemplate.from_template(template)
        rag_chain = (prompt | self.llm | StrOutputParser())

        return rag_chain

    def generate_answer(self, question: str, companyName: str, talent: str, job: str, limit: str, context: str):
        # chain에 입력을 전달하여 RAG 모델에서 답변 생성
        
        inputs = {
            "question": question,
            "company": companyName,
            "talent": talent,
            "job": job,
            "limit": limit,
            "context": context,
            
        }

        response = self.chain.invoke(inputs)
        return response
