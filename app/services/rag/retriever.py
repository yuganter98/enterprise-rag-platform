from typing import List, Dict, Optional
from langchain_core.documents import Document
from app.services.rag.vector_store import get_vector_store

def search_documents(query: str, role: str, top_k: int = 3) -> List[Document]:
    """
    Searches the vector store for documents relevant to the query.
    Applies RBAC filtering based on the user's role.
    """
    vector_store = get_vector_store()
    if not vector_store:
        return []

    # RBAC Logic:
    # If role is 'admin', they might see everything, but for this strict implementation
    # let's assume valid filters.
    # Note: FAISS filter syntax depends on the underlying store.
    # LangChain FAISS `search_kwargs={'filter': {'role': role}}` works for exact match.
    
    # Simple logic: If admin, maybe no filter? Or strict matching?
    # Let's stick to the requested "Filter results using metadata".
    # We will assume documents are tagged with the roles allowed to see them,
    # OR we filter by documents explicitly owned/visible to that role.
    # For simplicity in this step: We filter for documents where metadata['role'] matches.
    
    # If the user is admin, let's say they can see everything (no filter).
    search_kwargs = {"k": top_k}
    
    if role != "admin":
        # Only show docs where the doc's role matches the user's role
        # (This implies a document is tagged "This is for employees")
        search_kwargs["filter"] = {"role": role}

    # Perform similarity search
    docs = vector_store.similarity_search(query, **search_kwargs)
    return docs
