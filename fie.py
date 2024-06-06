from dotenv import load_dotenv 
load_dotenv()
from  PayPlan import PayPlan_Graph
from  CRAG import CRAG_Graph
from langchain_community.document_loaders import TextLoader ,PyPDFLoader

# bot = CRAG_Graph()
# answare =  bot.invoke(question ='piano pagamento, mi servono i valori e le data', history = [] , path= 'Data' )
# print(answare['answer'])

bot = CRAG_Graph()
answare =  bot.invoke(question ='piano pagamento, mi servono i valori da pagare e le date', history = [] , path= 'Data' )
print(answare['answer'])

# bot = PayPlan_Graph()
# pdf_contratto = PyPDFLoader(file_path='Data\CONTRATTO DI APPALTO.pdf')
# Docts_contratto = pdf_contratto.load()

# pdf_invoice = PyPDFLoader(file_path='Data\Fattura.pdf')
# Docts_invoice = pdf_contratto.load()

# answare =  bot.invoke(invoice= Docts_invoice, agreement= Docts_contratto)
# print(answare['answer'])