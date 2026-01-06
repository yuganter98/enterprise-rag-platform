import os
import pandas as pd
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader, DataFrameLoader
from langchain_core.documents import Document

def load_document(file_path: str) -> List[Document]:
    """
    Loads a document from the given file path.
    Supports .pdf, .txt, .docx, .csv, and .xlsx files.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    elif ext == ".csv":
        try:
            loader = CSVLoader(file_path, encoding="utf-8")
            # Dry run to check encoding
            loader.load()
        except UnicodeDecodeError:
            print("UTF-8 failed, retrying with latin-1")
            loader = CSVLoader(file_path, encoding="latin-1")
    elif ext == ".xlsx":
        # For Excel, we use pandas to read and DataFrameLoader to convert
        try:
            df = pd.read_excel(file_path)
            # Use all columns as page_content by default or specific ones?
            # We'll stick to page_content_column if we knew it, but here we load entire row content.
            loader = DataFrameLoader(df, page_content_column=df.columns[0] if not df.empty else "content")
        except Exception as e:
            raise ValueError(f"Failed to load Excel file: {str(e)}")
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return loader.load()
