from pathlib import Path
from typing import Optional
from .llm_client import chat
from .validation import parse_and_validate, build_retry_prompt
from .schemas import ExtractedDoc

PROMPT_EXTRACT = Path("prompts/extract.txt").read_text(encoding="utf-8")


def render(template: str, **kwargs) -> str:
    out = template
    for k, v in kwargs.items():
        out = out.replace(f"{{{{{k}}}}}", v or "")  # prints out {{TEXT}} bc {{ = {
    return out


async def extract_document(text: str, doc_type_hint: Optional[str] = None) -> ExtractedDoc:
    prompt = render(PROMPT_EXTRACT, TEXT=text, DOC_TYPE_HINT=(doc_type_hint or ""))

    raw = await chat(prompt)
    try:
        return parse_and_validate(raw)
    except Exception as e:
        retry_prompt = build_retry_prompt(prompt, str(e), raw)
        raw2 = await chat(retry_prompt)
        return parse_and_validate(raw2)
