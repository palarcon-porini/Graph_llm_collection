from langchain_openai import  AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os 

question_rewriter_prompt = PromptTemplate(
    template="""You a question re-writer that converts an input question to a better version that is optimized \n 
     for vectorstore retrieval. Look at the initial and formulate an improved question. \n
     Here is the initial question: \n\n {question}. answer in Italian ,Improved question with no preamble: \n """,
    input_variables=["generation", "question"],
)


retrieval_grader_prompt = PromptTemplate(
    template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
    Here is the retrieved document: \n\n {document} \n\n
    Here is the user question: {question} \n
    If the document contains keywords related to the user question, grade it as relevant. \n
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
    Provide the binary score as a JSON with a single key 'score' and no premable or explaination.""",
    input_variables=["question", "document",'history'],
)

retrieval_grader_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a grader assessing relevance of a retrieved document and the history  to a user question",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", """ \n 
        Here is the retrieved document: \n\n {document} \n\n
        Here is the user question: {question} \n
        If the document contains keywords related to the user question, grade it as relevant. \n
        It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
        Provide the binary score as a JSON with a single key 'score' and no premable or explaination.""",)
        ])

rag_chain_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Sei un Chatbot e hai il compito di risposta alle domande in italiano. Utilizzate i seguenti elementi di contesto recuperati per rispondere alla domanda. Se non conoscete la risposta, dite semplicemente che non la conoscete.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", """Usate al massimo tre frasi e mantenete la risposta concisa.""",),
        ("human", """\nDomanda: {question} \Contesto: {context} \Risposta:""",)
        
    ]
)

class llm_chian:
    def __init__(self, prompt,llm_model) -> None:
        self.prompt = prompt
        self.llm_model = llm_model
        pass
     
    def chain(self):
        self.question_rewriter = self.prompt | self.llm_model | StrOutputParser()

    def invoke(self,input):
        try:
          return self.question_rewriter.invoke(input)
        except:
          self.chain()
          return self.question_rewriter.invoke(input)

llm = AzureChatOpenAI(temperature=0, model_name=os.environ['DEPLOYMENT_NAME'])
question_rewriter = llm_chian(prompt=question_rewriter_prompt,llm_model=llm)
rag_chain = llm_chian(prompt=rag_chain_prompt,llm_model=llm)
retrieval_grader = llm_chian(prompt=retrieval_grader_prompt,llm_model=llm)