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
    start : Callable
    base_generate: Callable
    split_documents :  Callable
    decide_to_generate : Callable

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question : str
        content_list : str
        answer : str
        agreement : List[str]
    """
    answer : str
    invoice : List[str]
    agreement : List[str]

class Graph:
    def __init__(self,nodes : Node,  *args) -> None:
        self.nodes = nodes
        self.workflow = StateGraph(GraphState)
        self.Define_the_nodes()
        self.Build_graph()
        self.Complite_()
    
    def Define_the_nodes(self):
        self.workflow.add_node('START', self.nodes['START'])  # retrieve
        self.workflow.add_node('BASE_GENERATE', self.nodes['BASE_GENERATE'])  # grade documents
        self.workflow.add_node('SPLIT_DOCUMENTS', self.nodes['SPLIT_DOCUMENTS'])  # generatae
    
    def Build_graph(self):
        self.workflow.set_entry_point("START")
        self.workflow.add_conditional_edges("START",self.nodes['DECIDE_TO_GENERATE'])
        self.workflow.add_edge('SPLIT_DOCUMENTS','BASE_GENERATE')
        self.workflow.add_edge('BASE_GENERATE',END)

    def Complite_(self):
        self.flow = self.workflow.compile()

    def invoke(self,inputs):
        return self.flow.invoke(inputs)
