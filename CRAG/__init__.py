import CRAG.Function as f
from CRAG.Graph import Graph ,Node
from CRAG import Function 
from CRAG import Graph
from CRAG import LLM

class CRAG_Graph:
    def __init__(self) -> None:
        self.node : Node = {'RETRIEVE' : f.RETRIEVE,
                            'GRADE_DOCUMENTS': f.GRADE_DOCUMENTS,
                            'GENERATE' : f.GENERATE,
                            'TRANSFORM_QUERY' : f.TRANSFORM_QUERY,
                            }
        self.graph = Graph(self.node,condition_funct = f.DECIDE_TO_GENERATE)

    def invoke(self, question : str, history : list, path : str):
        return self.graph.invoke({'question': question,'history':history , 'path':path})
