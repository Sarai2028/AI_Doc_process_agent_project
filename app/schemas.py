from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional

# limits doc types to a known set, prevents random strings
DocType = Literal["invoice", "resume", "contract", "other"]


class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=20)  # must be at least 20 char to prevent garbage input
    document_type: Optional[DocType] = None


class ExtractedDoc(BaseModel):
    doc_type: DocType  # enforced to one of the allowed values
    fields: Dict[str, str]  # dictionary of extracted fields, strings only
    confidence: float = Field(..., ge=0.0, le=1.0)
    issues: List[str] = Field(default_factory=list) # list of extraction issues i.e. missing fields, unclear totals


class ExtractResponse(BaseModel):  # wraps result in stable response object
    result: ExtractedDoc
