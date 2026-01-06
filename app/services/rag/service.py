from app.services.rag.loader import load_document
from app.services.rag.chunker import chunk_text
from app.services.rag.vector_store import add_documents_to_index

def ingest_document(file_path: str, title: str, user_id: int, role: str):
    """
    Orchestrates the ingestion process:
    1. Load document
    2. Chunk text
    3. Add metadata (title, user permissions)
    4. Embed and store in FAISS
    """
    # 1. Load
    raw_docs = load_document(file_path)
    
    # 2. Chunk
    chunks = chunk_text(raw_docs)
    
    # 3. Enhance Metadata
    for chunk in chunks:
        chunk.metadata["title"] = title
        chunk.metadata["user_id"] = user_id
        chunk.metadata["role"] = role  # IMPORTANT: For future RBAC filtering
        # chunk.metadata["source"] is usually already set by loader
        
    # 4. Store
    add_documents_to_index(chunks)
    
    return len(chunks)
