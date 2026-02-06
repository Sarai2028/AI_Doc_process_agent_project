import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"  # llama3


class LLMError(Exception):
    pass


async def chat(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(OLLAMA_URL, json=payload)
        if r.status_code != 200:
            raise LLMError(f"Ollama error: {r.text}")
        data = r.json()
        return data["response"]