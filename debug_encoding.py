import os
from app.services.rag.service import ingest_document

# Create ANSI CSV
filename = "debug_ansi.csv"
with open(filename, "w", encoding="mbcs") as f: # mbcs is Windows ANSI
    f.write("name,role\nÉlève,Student")

try:
    print("Testing ANSI CSV ingestion...")
    chunks = ingest_document(filename, title=filename, user_id=1, role="admin")
    print(f"Success! Ingested {chunks} chunks.")
except Exception as e:
    print("ANSI CRASH DETECTED!")
    print(e)
finally:
    if os.path.exists(filename):
        os.remove(filename)
