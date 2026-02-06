import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from .schemas import ExtractRequest, ExtractResponse
from .agent import extract_document

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("doc-agent")


app = FastAPI(title="AI Document Processing Agent")  # creates the web server application


class ExtractRequest(BaseModel):
    text: str
    document_type: Optional[str] = None


# when an HTTP GET request to /health is requested, run health() function
@app.get("/health")  # health endpoint to prove service is alive without touching the model/llm
def health():
    return {"status": "ok"}


@app.post("/extract", response_model=ExtractResponse)  # defines endpoint that will do the work
# FastAPI use to validate outgoing responses, enforce contract compliance
async def extract(req: ExtractRequest):  # async bc LLM calls are network calls, async allows better concurrency
    # temp placeholder so endpoint works
    # replace with LLM + validation agent
    logger.info("Received extract request len=%s", len(req.text))
    try:
        result = await extract_document(req.text, req.document_type)
        logger.info("Done doc_type=%s confidence=%.2f", result.doc_type, result.confidence)
        return ExtractResponse(result=result)
    except Exception as e:
        logger.exception("Extraction failed")
        raise HTTPException(status_code=500, detail=str(e))  # if it fails, log the stack trace and return http 500




