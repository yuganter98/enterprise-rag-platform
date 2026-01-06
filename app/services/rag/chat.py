from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.services.rag.retriever import search_documents
from app.services.rag.llm import get_llm
from app.services.rag.prompt import rag_prompt

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def answer_question(query: str, role: str) -> str:
    """
    Orchestrates the RAG flow:
    1. Retrieve relevant docs (filtered by role).
    2. Construct prompt.
    3. Generate answer using LLM.
    """
    # 1. Retrieve
    docs = search_documents(query, role)
    
    if not docs:
        return "I couldn't find any relevant documents to answer your question."

    # 2. Setup Chain
    llm = get_llm()
    formatted_context = format_docs(docs)
    
    # We can use a simple LCEL chain or manual invocation
    # Manual invocation for clarity and control:
    prompt_value = rag_prompt.format(context=formatted_context, question=query)
    
    # 3. Generate
    response = llm.invoke(prompt_value)
    
    # Extract content if it's an AIMessage, otherwise return as string
    if hasattr(response, "content"):
        return response.content
    return str(response)
