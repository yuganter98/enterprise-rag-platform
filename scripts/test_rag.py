from app.services.rag.chat import answer_question

# Simulated run
print("Running RAG Test...")
try:
    response = answer_question("What is the leave policy?", role="employee")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")
