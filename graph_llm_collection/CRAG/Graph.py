from langchain_core.output_parsers import StrOutputParser
from typing_extensions import TypedDict
from typing import TypedDict, Callable
from typing import List
from langgraph.graph import END, StateGraph

class Node(TypedDict):
    """
    Represents the nodes of our graph.

    Attributes:
        retrieve: retrieve document
        grade_documents: chain grade_documents
        generate: chain generate
        transform_query: chain transform_query
        web_search : chain web_search
    """
    retrieve : Callable
    grade_documents: Callable
    generate : Callable
    transform_query : Callable

class Node_seach(TypedDict):
    """
    Represents the nodes of our graph.

    Attributes:
        retrieve: retrieve document
        grade_documents: chain grade_documents
        generate: chain generate
        transform_query: chain transform_query
        web_search : chain web_search
    """
    retrieve : Callable
    grade_documents: Callable
    grade_documents_search :  Callable

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        answer: LLM generation
        web_search: whether to add search
        documents: list of documents 
    """
    question : str
    filtri: List[str]
    answer : str
    path : str  
    flag_relevant_document : str
    history : List[dict]
    documents : List[str]

class CRAG_seach:
    def __init__(self,nodes : Node_seach ,condition_funct , *args) -> None:
        self.nodes=nodes
        self.seach = StateGraph(GraphState)
        self.Define_the_nodes_search()
        self.Build_graph_search()
        self.Complite_()
    
    def Define_the_nodes_search(self):
        self.seach.add_node("retrieve",  self.nodes['retrieve'])  # retrieve
        self.seach.add_node("grade_documents_search", self.nodes['grade_documents_search'])  # grade documents

    def Build_graph_search(self):
        self.seach.set_entry_point("retrieve")
        self.seach.add_edge("retrieve", "grade_documents_search")
        self.seach.add_edge("grade_documents_search", END)

    def Complite_(self):
        self.app_search = self.seach.compile()

    def invoke(self,inputs):
        return self.app_search.invoke(inputs)


class Graph:
    def __init__(self,nodes : Node,condition_funct , *args) -> None:
        self.nodes=nodes
        self.workflow = StateGraph(GraphState)
        self.Define_the_nodes()
        self.Build_graph(condition_funct)
        self.Complite_()
    
    def Define_the_nodes(self):
        self.workflow.add_node("retrieve",  self.nodes['retrieve'])  # retrieve
        self.workflow.add_node("grade_documents", self.nodes['grade_documents'])  # grade documents
        self.workflow.add_node("generate", self.nodes['generate'])  # generatae
        self.workflow.add_node("transform_query", self.nodes['transform_query'])  # transform_query
    
    def Build_graph(self,decide_to_generate):
        self.workflow.set_entry_point("retrieve")
        self.workflow.add_edge("retrieve", "grade_documents")
        self.workflow.add_conditional_edges(
            "grade_documents",
            decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate",
            },
        )
        self.workflow.add_edge("transform_query","generate")
        self.workflow.add_edge("generate", END)

    def Define_the_nodes(self):
        self.workflow.add_node("RETRIEVE",  self.nodes['RETRIEVE'])  # retrieve
        self.workflow.add_node("GRADE_DOCUMENTS", self.nodes['GRADE_DOCUMENTS'])  # grade documents
        self.workflow.add_node("GENERATE", self.nodes['GENERATE'])  # generatae
        self.workflow.add_node("TRANSFORM_QUERY", self.nodes['TRANSFORM_QUERY'])  # transform_query
    
    def Build_graph(self,decide_to_generate):
        self.workflow.set_entry_point("RETRIEVE")
        self.workflow.add_edge("RETRIEVE", "GRADE_DOCUMENTS")
        self.workflow.add_conditional_edges(
            "GRADE_DOCUMENTS",
            decide_to_generate,
            {
                "TRANSFORM_QUERY": "TRANSFORM_QUERY",
                "GENERATE": "GENERATE",
            },
        )
        self.workflow.add_edge("TRANSFORM_QUERY","GENERATE")
        self.workflow.add_edge("GENERATE", END)

    def Complite_(self):
        self.app = self.workflow.compile()

    def invoke(self,inputs):
        return self.app.invoke(inputs)