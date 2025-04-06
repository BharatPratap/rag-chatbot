from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub
from langchain.chains import RetrievalQA

from dotenv import load_dotenv
load_dotenv()

# Load embeddings + vectorstore
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("data/faiss_store", embedding_model, allow_dangerous_deserialization=True)

# Load retriever
retriever = db.as_retriever(search_kwargs={"k": 4})

retrieved_docs = retriever.get_relevant_documents("How can I create my UPI ID?")
for doc in retrieved_docs:
    print(doc.page_content)
    print("\n\n\n")