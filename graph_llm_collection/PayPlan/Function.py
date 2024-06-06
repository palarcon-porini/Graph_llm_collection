import tiktoken
from langchain_text_splitters.character import CharacterTextSplitter
from langchain.docstore.document import Document
import graph_llm_collection.PayPlan.LLM as llm

def START(state):
    print("---ASSESS START---")
    invoice = state["invoice"]
    documents = state["agreement"]
    documents_text = '\n'.join([str(d.metadata['page'])+'\n'+d.page_content for d in  documents])
    invoice_Text = '\n'.join([str(d.metadata['page'])+'\n'+d.page_content for d in  invoice])
    return {"invoice": invoice_Text, "agreement": documents_text}

def DECIDE_TO_GENERATE(state):
    invoice = state["invoice"]
    documents = state["agreement"]
    
    enco = tiktoken.get_encoding('cl100k_base')
    if len(enco.encode(documents+'\n'+invoice)) <= 13000:
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print("---DECISION: BASE_GENERATE---")
        return "BASE_GENERATE"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: SPLIT_DOCUMENTS---")
        return "SPLIT_DOCUMENTS"
    
def BASE_GENERATE(state):
    invoice = state["invoice"]
    documents = state["agreement"]
    piano_pagmenti = llm.LLM_PayPlane.invoke({'context':documents,'invoice' : invoice , 'domanda':'fai un piano di pagamento, Descrivi i limiti, scadenze importo da pagare ,con date specifiche'}).content
    return {'answer': piano_pagmenti}

def SPLIT_DOCUMENTS(state):
    documents = state["agreement"]
    invoice = state["invoice"]
    enco = tiktoken.get_encoding('cl100k_base')

    def splt(text):
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(encoding_name="cl100k_base", chunk_size=14000, chunk_overlap=100)
        chunks = text_splitter.split_text(text)
        return chunks
    
    def Summary_(context):
        Summary = llm.LLM_Text_processor.invoke({'context':context,'domanda':'Fai un riassunto accurato del contesto , tinieni presente che questo riassunto servira a creare un piano di pagmento' }) # TODO: summary of invoice 
        return Summary

    Summary_invoice = []
    if len(enco.encode(invoice)) <= 10000:
        invoice = splt(invoice) #  List[str]
        for iv in invoice:
           Summary  = Summary_(iv)
           Summary_invoice.append(Summary)
    else:
        Summary_invoice.append(invoice)

    Summary_documents = []
    if len(enco.encode(documents)) <= 13000:
        documents = splt(documents)
        for iv in documents:
           Summary  = Summary_(iv)
           Summary_documents.append(Summary)
        pass
    else:
        Summary_documents.append(documents)
    
    invoice = Document(page_content=Summary_invoice)
    documents = Document(page_content=Summary_documents)
    return {"invoice": invoice, "agreement": documents}