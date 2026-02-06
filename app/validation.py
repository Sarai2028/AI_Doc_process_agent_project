import json
from .schemas import ExtractedDoc


def parse_and_validate(raw: str) -> ExtractedDoc:
    raw = raw.strip()
    obj = json.loads(raw)
    return ExtractedDoc.parse_obj(obj)


def build_retry_prompt(original_prompt: str, error_msg: str, bad_output: str) -> str:
    return(
        original_prompt
        + "\n\nYour previous output was INVALID.\n"
        + f"Validation error: {error_msg}\n"
        + "Bad output:\n"
        + bad_output
        + "\n\nReturn only corrected valid JSON. No markdown."
    )
