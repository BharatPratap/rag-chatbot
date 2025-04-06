import os
import glob
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def load_texts(text_folder):
    texts = []
    metadata = []
    for path in glob.glob(f"{text_folder}/*.txt"):
        with open(path, "r") as f:
            content = f.read()
        chunks = chunk_text(content)
        texts.extend(chunks)
        metadata.extend([os.path.basename(path)] * len(chunks))
    return texts, metadata

def embed_texts(texts):
    model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts, model)
    vectorstore.save_local("data/faiss_store")
    return

def save_faiss_index(embeddings, texts, metadata, output_path="data/faiss_store"):
    os.makedirs(output_path, exist_ok=True)
    
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, os.path.join(output_path, "index.faiss"))
    with open(os.path.join(output_path, "store.pkl"), "wb") as f:
        pickle.dump({"texts": texts, "metadata": metadata}, f)

def run_embedding_pipeline():
    texts, metadata = load_texts("data/web")
    embeddings = embed_texts(texts)
    # save_faiss_index(embeddings, texts, metadata)

if __name__ == "__main__":
    run_embedding_pipeline()
