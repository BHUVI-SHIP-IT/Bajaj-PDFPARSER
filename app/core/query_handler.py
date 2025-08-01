from app.core.document_parser import load_pdf_from_url
from app.services.embeddings import get_embedding_model
from app.services.vector_store import get_vectorstore, load_vectorstore
from app.services.openai_llm import get_llm, get_qa_chain
from app.utils.logger import get_logger
import os

VECTORSTORE_DIR = "vectorstore_test"
logger = get_logger("query_handler")

def process_document_and_answer(documents: str, questions: list[str]) -> list[str]:
    try:
        logger.info(f"Processing document: {documents}")
        
        # Step 1: Load PDF pages
        pages = load_pdf_from_url(documents)
        logger.info(f"Loaded {len(pages)} pages from document.")

        # Step 2: Initialize embedding model
        embedding_model = get_embedding_model()

        # Step 3: Load or create vector store
        vectordb_path = os.path.join(VECTORSTORE_DIR, "chroma.sqlite3")
        if not os.path.exists(vectordb_path):
            logger.info("Vectorstore not found. Creating new index.")
            vectordb = get_vectorstore(pages, embedding_model)
        else:
            logger.info("Loading existing vectorstore.")
            vectordb = load_vectorstore(embedding_model)

        # Step 4: Set up LLM + QA chain
        llm = get_llm()
        qa_chain = get_qa_chain(llm, vectordb)

        # Step 5: Run QA chain on each question
        answers = []
        for q in questions:
            try:
                answer = qa_chain.run(q)
                logger.info(f"Q: {q} => A: {answer}")
                answers.append(answer)
            except Exception as e:
                logger.error(f"Error answering question: {q} | {e}")
                answers.append("Could not answer this question.")

        return answers

    except Exception as e:
        logger.error(f"Failed to process document: {e}")
        return ["Error processing document."]
