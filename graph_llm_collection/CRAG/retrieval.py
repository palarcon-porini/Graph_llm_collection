from langchain_community.document_loaders import TextLoader ,PyPDFLoader
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os 
# Load the document, split it into chunks, embed each chunk and load it into the vector store.


class Ratrieval:
    def __init__(self ,path : str):
        self.path = path
        raw_documents = self.load_documents()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
        documents = text_splitter.split_documents(raw_documents)
        db = FAISS.from_documents(documents, AzureOpenAIEmbeddings(model='ada'))
        self.ratrieval = db
        pass
    
    def load_type(self):
        if self.path.endswith('.pdf'):
            return PyPDFLoader(self.path).load()
        else:
            return TextLoader(self.path).load()
        
    def load_documents(self):
        ''' carica multi documenti, la funzione accetta .txt e .pdf '''
        if os.path.isdir(self.path):
            documents = []
            for file in os.listdir(self.path):
                file_path = os.path.join(self.path, file)
                if file_path.endswith('.pdf'):
                    documents.extend(PyPDFLoader(file_path).load())
                elif file_path.endswith('.txt'):
                    documents.extend(TextLoader(file_path).load())
            return documents
        else:
            return self.load_type()
    
    def invoke(self, query):
        return  self.ratrieval.similarity_search(query)