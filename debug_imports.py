import sys
print("Checking docx2txt...")
try:
    import docx2txt
    print("docx2txt OK")
except ImportError as e:
    print(f"docx2txt FAILED: {e}")

print("Checking openpyxl...")
try:
    import openpyxl
    print("openpyxl OK")
except ImportError as e:
    print(f"openpyxl FAILED: {e}")

print("Checking pandas...")
try:
    import pandas
    print("pandas OK")
except ImportError as e:
    print(f"pandas FAILED: {e}")

print("Checking LangChain CSVLoader...")
try:
    from langchain_community.document_loaders import CSVLoader
    print("CSVLoader OK")
except ImportError as e:
    print(f"CSVLoader FAILED: {e}")

print("Checking LangChain Docx2txtLoader...")
try:
    from langchain_community.document_loaders import Docx2txtLoader
    print("Docx2txtLoader OK")
except ImportError as e:
    print(f"Docx2txtLoader FAILED: {e}")

print("Checking LangChain DataFrameLoader...")
try:
    from langchain_community.document_loaders import DataFrameLoader
    print("DataFrameLoader OK")
except ImportError as e:
    print(f"DataFrameLoader FAILED: {e}")
