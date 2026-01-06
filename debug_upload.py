import sys
import os

# Create a dummy CSV
with open("test.csv", "w") as f:
    f.write("col1,col2\nval1,val2")

try:
    print("Attempting to import loader...")
    from app.services.rag.loader import load_document
    print("Import successful.")

    print("Attempting to load CSV...")
    docs = load_document("test.csv")
    print(f"Loaded {len(docs)} docs.")
    print("Content:", docs[0].page_content)

except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    if os.path.exists("test.csv"):
        os.remove("test.csv")
