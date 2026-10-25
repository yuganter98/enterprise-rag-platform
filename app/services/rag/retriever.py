from typing import Any, Dict, List
from langchain_core.documents import Document
from app.services.rag.vector_store import get_vector_store


def can_role_see(metadata: Dict[str, Any], role: str) -> bool:
    """
    Returns True if a chunk with this metadata is visible to the given role.

    New chunks carry `allowed_roles` (the audience chosen at upload time).
    Chunks ingested before that field existed only carry the uploader's
    `role`, so for those we keep the old exact-match behaviour.
    """
    allowed_roles = metadata.get("allowed_roles")
    if allowed_roles is not None:
        return role in allowed_roles
    return metadata.get("role") == role


def search_documents(query: str, role: str, top_k: int = 3) -> List[Document]:
    """
    Searches the vector store for documents relevant to the query.
    Applies RBAC filtering based on the user's role.
    """
    vector_store = get_vector_store()
    if not vector_store:
        return []

    # Admins can see everything, so no filter is needed.
    search_kwargs = {"k": top_k}

    if role != "admin":
        search_kwargs["filter"] = lambda metadata: can_role_see(metadata, role)
        # FAISS filters after the nearest-neighbour search, so fetch a wider
        # candidate pool to still end up with `top_k` visible chunks.
        search_kwargs["fetch_k"] = top_k * 20

    docs = vector_store.similarity_search(query, **search_kwargs)
    return docs
