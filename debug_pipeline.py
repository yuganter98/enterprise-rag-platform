import os
import shutil
from app.services.rag.service import ingest_document

# Setup dummy CSV
filename = "debug_data.csv"
with open(filename, "w") as f:
    f.write("name,role,description\nAlice,Engineer,Works on backend.\nBob,Designer,Works on frontend.")

try:
    print("Starting ingestion test...")
    # Mock user_id and role
    chunks = ingest_document(filename, title=filename, user_id=1, role="admin")
    print(f"Success! Ingested {chunks} chunks.")
except Exception as e:
    print("CRASH DETECTED!")
    import traceback
    traceback.print_exc()
finally:
    if os.path.exists(filename):
        os.remove(filename)
