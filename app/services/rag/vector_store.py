import os
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Path to store the FAISS index locally
VECTOR_STORE_PATH = os.path.join(os.getcwd(), "data", "vector_store")

def get_embeddings():
    """Returns the HuggingFace embedding model."""
    # This downloads the model locally on first use (~80MB)
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_vector_store():
    """Loads existing FAISS index or creates a new one if not found."""
    embeddings = get_embeddings()
    if os.path.exists(VECTOR_STORE_PATH):
        return FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
    return None

def add_documents_to_index(documents: List[Document]):
    """
    Adds documents to the local FAISS index and persists it.
    """
    embeddings = get_embeddings()
    
    if os.path.exists(VECTOR_STORE_PATH):
        vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_documents(documents)
    else:
        vector_store = FAISS.from_documents(documents, embeddings)
    
    # Save to disk
    vector_store.save_local(VECTOR_STORE_PATH)
