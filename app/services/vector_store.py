from langchain_community.vectorstores import Chroma
from app.utils.logger import get_logger
import os

CHROMA_DIR = "vectorstore_test"
logger = get_logger("vector_store")

def get_vectorstore(pages, embedding_model):
    try:
        vectordb = Chroma.from_documents(
            documents=pages,
            embedding=embedding_model,
            persist_directory=CHROMA_DIR
        )
        vectordb.persist()
        logger.info("Vector store created and persisted successfully.")
        return vectordb
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        raise

def load_vectorstore(embedding_model):
    try:
        logger.info("Loading existing vector store from disk.")
        return Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding_model)
    except Exception as e:
        logger.error(f"Error loading vector store: {e}")
        raise