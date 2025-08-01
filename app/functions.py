from app.core.document_parser import load_pdf_from_path
from app.services.embeddings import get_embedding_model
from app.services.vector_store import get_vectorstore, load_vectorstore
from app.services.openai_llm import get_llm, get_qa_chain
import os

def process_document_and_answer(document_path, questions):
    embedding_model = get_embedding_model()

    # Step 1: Parse PDF
    pages = load_pdf_from_path(document_path)

    # Step 2: Create or Load VectorStore
    if not os.path.exists("vectorstore_test/chroma.sqlite3"):
        vectordb = get_vectorstore(pages, embedding_model)
    else:
        vectordb = load_vectorstore(embedding_model)

    # Step 3: LLM + QA Chain
    llm = get_llm()
    qa_chain = get_qa_chain(llm, vectordb)

    # Step 4: Ask questions
    answers = []
    for question in questions:
        result = qa_chain.run(question)
        answers.append(result)
    
    return answers
