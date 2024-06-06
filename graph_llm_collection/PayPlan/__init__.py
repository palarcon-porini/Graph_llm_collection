import graph_llm_collection.PayPlan.Function as f
from graph_llm_collection.PayPlan.Graph import Graph ,Node
from langchain_core.documents.base import Document

class PayPlan_Graph:
    def __init__(self) -> None:
        self.node : Node = {
            'START': f.START,
            'BASE_GENERATE': f.BASE_GENERATE,
            'SPLIT_DOCUMENTS': f.SPLIT_DOCUMENTS,
            'DECIDE_TO_GENERATE': f.DECIDE_TO_GENERATE,
        }
        self.graph = Graph(self.node)

    def invoke(self, invoice : list[Document] , agreement : list[Document]):
        return self.graph.invoke({'invoice':invoice,'agreement':agreement})
