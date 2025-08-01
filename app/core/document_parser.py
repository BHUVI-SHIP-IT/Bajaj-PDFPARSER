from langchain_community.document_loaders import PyPDFLoader
import tempfile
import requests
import os
from app.utils.logger import get_logger

logger = get_logger("document_parser")

def load_pdf_from_path(file_path: str):
    try:
        loader = PyPDFLoader(file_path)
        return loader.load_and_split()
    except Exception as e:
        logger.error(f"Failed to parse PDF at {file_path}: {e}")
        return []

def load_pdf_from_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name

        pages = load_pdf_from_path(tmp_path)
        return pages

    except Exception as e:
        logger.error(f"Failed to download or parse PDF from {url}: {e}")
        return []
    
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
