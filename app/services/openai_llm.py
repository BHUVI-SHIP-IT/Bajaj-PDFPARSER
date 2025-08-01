import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from app.utils.logger import get_logger

load_dotenv()
logger = get_logger("openrouter_llm")

def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("OPENROUTER_API_KEY not found in environment variables.")
        raise ValueError("Missing OpenRouter API key")

    logger.info("Initializing OpenRouter LLM: openai/o4-mini-high")
    return ChatOpenAI(
        model="openai/o4-mini-high",                  # ✅ or any other OpenRouter-supported model
        temperature=0,
        openai_api_key=api_key,
        base_url="https://openrouter.ai/api/v1",# ✅ critical for OpenRouter
        max_tokens=500,
    )

def get_qa_chain(llm, vectordb):
    logger.info("Creating RetrievalQA chain")
    return RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())
