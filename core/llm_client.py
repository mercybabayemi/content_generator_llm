import json
#import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from core.config import settings
#import re


#load_dotenv()

# Initialize client once (avoid reconnecting every request)
_client: AsyncOpenAI | None = None


def init_llm() -> AsyncOpenAI:
    """Initialize and return the LLM client."""
    global _client

    if _client is None:
        _client = AsyncOpenAI(
            base_url=settings.ollama_base_url, #os.getenv("OLLAMA_BASE_URL"),
            api_key=settings.api_key #os.getenv("API_KEY")
        )

    return _client


async def call_llm(system: str, user: str, model: str = "phi3.5") -> dict:
    """Send a prompt to the LLM and return parsed JSON."""

    client = init_llm()

    response = await client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    raw = response.choices[0].message.content
   # cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()

    try:
         return json.loads(raw)
   #     return json.loads(cleaned)

    except json.JSONDecodeError as e:
        raise ValueError(
        f"LLM did not return  valid JSON. \n"
        f"JSON parse error: {e}"
        f"Raw response: {raw}"
        )
