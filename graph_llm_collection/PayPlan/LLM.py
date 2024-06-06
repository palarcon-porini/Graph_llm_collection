from langchain_openai import  AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

prompt_PayPlane = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "leggi attentanente, \n"
            "considera il contesto : {context} \n"
            "considera il la fattura : {invoice} \n"
            'rispondi in modo coerente e preciso : {domanda} \n'
            
            ,
        ),
    ]
)

llm = AzureChatOpenAI(model="gpt35_16k",temperature=0)
LLM_PayPlane = prompt_PayPlane | llm

prompt_Text_processor = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "leggi attentanente, \n"
            "considera il contesto : {context} \n"
            'rispondi in modo coerente e preciso : {domanda} \n'
            
            ,
        )
    ]
)

llm = AzureChatOpenAI(model="gpt35_16k",temperature=0)
LLM_Text_processor  = prompt_Text_processor | llm