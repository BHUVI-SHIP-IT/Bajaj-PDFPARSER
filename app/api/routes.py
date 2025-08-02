from fastapi import APIRouter, Header, HTTPException, status
from app.models.schema import QueryRequest, QueryResponse
from app.core.query_handler import process_document_and_answer
from app.utils.logger import get_logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EXPECTED_TOKEN = os.getenv("AUTH_TOKEN")

router = APIRouter()
logger = get_logger("router")

@router.post("api/v1/hackrx/run", response_model=QueryResponse)
def run_query(
    request: QueryRequest,
    authorization: str = Header(None)
):
    # Check Authorization header
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Missing or malformed Authorization header.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    
    token = authorization.split(" ")[1]
    if token != EXPECTED_TOKEN:
        logger.warning("Invalid token received.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

    logger.info(f"Authenticated request for document: {request.documents}")
    
    answers = process_document_and_answer(request.documents, request.questions)
    return QueryResponse(answers=answers)
