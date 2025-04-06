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

# Prompt: add "I don't know" fallback
prompt_template = """
You are a helpful support chatbot. Use the context to answer the question.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"], model_kwargs={})

# Use HF Inference API (replace with LLM of your choice)
llm = HuggingFaceHub(
    repo_id="teapotai/teapotllm",
    model_kwargs={"temperature":0.5, "max_length":1500, }, task='text-generation')


qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt},
)

if __name__ == "__main__":
    while True:
        question = input("Ask: ")
        if question.lower() in ["exit", "quit"]:
            break
        result = qa_chain(question)
        print(prompt_template)
        print("Answer:", result["result"])
