from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()

class RagPipeline:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
        self.chain = self.init_chain()

    def init_chain(self):
        template = """
        당신은 자기소개서 작성 도우미입니다. 
        당신은 나에 대해서 굉장히 잘 알고 있습니다.
        나는 해당 기업에 입사하기 위해 자기소개서를 작성하고 있습니다.
        해당 질문에 대한 답변에 대해 다음 규칙을 지켜 작성해주세요. 
        답변은 반드시 글자수 {limit} 미만으로 작성해주세요.

        # 지원 기업:
        {company}
        
        # 기업 인재상:
        {talent}
        
        # 지원 직무:
        {job}

        # 질문:
        {question}

        ### 답변:
        """

        prompt = PromptTemplate.from_template(template)
        rag_chain = (prompt | self.llm | StrOutputParser())

        return rag_chain

    def generate_answer(self, question: str, companyName: str, talent: str, job: str, limit: str):
        # chain에 입력을 전달하여 RAG 모델에서 답변 생성
        
        inputs = {
            "question": question,
            "company": companyName,
            "talent": talent,
            "job": job,
            "limit": limit
        }

        response = self.chain.invoke(inputs)
        return response
