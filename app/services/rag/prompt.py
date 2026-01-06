from langchain_core.prompts import PromptTemplate

RAG_TEMPLATE_STR = """You are a helpful AI assistant for an enterprise.
Use the following pieces of context to answer the user's question.
If you don't know the answer based on the context, just say "I don't know", do not try to make up an answer.

Context:
{context}

Question:
{question}

Answer:"""

rag_prompt = PromptTemplate(
    template=RAG_TEMPLATE_STR,
    input_variables=["context", "question"]
)
