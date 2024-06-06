import graph_llm_collection.CRAG.Function as f
from graph_llm_collection.CRAG.Graph import Graph ,Node
from graph_llm_collection.CRAG import Function , retrieval
from graph_llm_collection.CRAG import Graph

class CRAG_Graph:
    '''
    You must to set Azure Openai API key in the environment variable
        import os

        os.environ['DEPLOYMENT_NAME'] = '**********'
        os.environ['AZURE_OPENAI_EMBEDDING_DEPLOYMENT'] = '**********'
        os.environ['AZURE_OPENAI_API_KEY'] = '**********'
        os.environ['OPENAI_API_VERSION'] = '**********'
        os.environ['AZURE_OPENAI_ENDPOINT'] = '**********'

    '''
    def __init__(self) -> None:
        self.node : Node = {'RETRIEVE' : f.RETRIEVE,
                            'GRADE_DOCUMENTS': f.GRADE_DOCUMENTS,
                            'GENERATE' : f.GENERATE,
                            'TRANSFORM_QUERY' : f.TRANSFORM_QUERY,
                            }
        self.graph = Graph(self.node,condition_funct = f.DECIDE_TO_GENERATE)

    def invoke(self, question : str, history : list, path : str):
        return self.graph.invoke({'question': question,'history':history , 'path':path})
