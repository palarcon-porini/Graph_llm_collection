import tiktoken
from langchain_text_splitters.character import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_core.messages import AIMessage, HumanMessage
from CRAG.LLM import llm ,question_rewriter, rag_chain, retrieval_grader
from CRAG.retrieval import Ratrieval

def RETRIEVE(state):
    print("---RETRIEVE---")
    query = state["question"]
    path = state["path"]
    db_r = Ratrieval(path=path)
    results = db_r.invoke(query)
    # for result in results:
    #     re.append(Document(page_content = result['chunk'], metadata = {'title':result['title'],'url':result['path']}))
    return {"documents": results, "question": query} 


def GENERATE(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    history = []
    for mess in state["history"]:
        if mess['type'] == 'bot':
            history.append(AIMessage(content=mess['mess']))
        else:
            history.append(HumanMessage(content=mess['mess']))
    documents_text = '\nDocumento: '.join([doc.page_content for doc in documents])
    # RAG generation
    answer = rag_chain.invoke({"context": documents_text, "question": question,'history':history})
    return {"documents": documents, "question": question, "answer": answer}

def GRADE_DOCUMENTS(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with only filtered relevant documents
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    history = []
    for mess in state["history"]:
        if mess['type'] == 'bot':
            history.append(AIMessage(content=mess['mess']))
        else:
            history.append(HumanMessage(content=mess['mess']))
    # Score each doc
    filtered_docs_true = []
    filtered_docs_false = []
    flag_relevant_document = "No"
    
    print(len(documents))
    count_relevant = 0
    for d in documents:
        if count_relevant == 6:
            break
        score = retrieval_grader.invoke({"question": question, "document": d.page_content,'history':history})
        grade = eval(score)['score']
        if grade == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            if d not in filtered_docs_true:
               count_relevant = 0
               filtered_docs_true.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            if d not in filtered_docs_false:
               count_relevant = count_relevant + 1 
               filtered_docs_false.append(d)
            
    if len(filtered_docs_true) > 0:
        filtered_docs = filtered_docs_true
        flag_relevant_document = 'No'
    else:
        filtered_docs = []
        flag_relevant_document = "yes"

    return {"documents": filtered_docs, "question": question, "flag_relevant_document": flag_relevant_document}

def grade_documents_search(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with only filtered relevant documents
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    
    # Score each doc
    filtered_docs = []
    flag_relevant_document = "Yes"
    print(len(documents))
    for d in documents:
        score = retrieval_grader.invoke({"question": question, "document": d.metadata['title'] })
        grade = eval(score)['score']
        if grade == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
            flag_relevant_document = "NO"
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            continue
    if flag_relevant_document:
            filtered_docs = documents
    return {"documents": filtered_docs, "question": question, "flag_relevant_document": flag_relevant_document}

def TRANSFORM_QUERY(state):
    """
    Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """

    print("---TRANSFORM QUERY---")
    question = state["question"]
    documents = state["documents"]

    # Re-write question
    better_question = question_rewriter.invoke({"question": question})
    return {"documents": documents, "question": better_question}
    


def DECIDE_TO_GENERATE(state):
    """
    Determines whether to generate an answer, or re-generate a question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """
    print("---ASSESS GRADED DOCUMENTS---")
    question = state["question"]
    flag_relevant_document = state["flag_relevant_document"]
    filtered_documents = state["documents"]

    if flag_relevant_document == "Yes":
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---")
        return "TRANSFORM_QUERY"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "GENERATE"