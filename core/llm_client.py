import json
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv()

load_dotenv()

# Initialize client once (avoid reconnecting every request)
_client: AsyncOpenAI | None = None


def init_llm() -> AsyncOpenAI:
    """Initialize and return the LLM client."""
    global _client

    if _client is None:
        _client = AsyncOpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL"),
            api_key=os.getenv("API_KEY")
        )

    return _client


async def call_llm(system: str, user: str, model: str = "phi3.5") -> dict:
    """Send a prompt to the LLM and return parsed JSON."""

    client = init_llm()

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    raw = response.choices[0].message.content

    try:
        return json.loads(raw)

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Raw response: {raw}")
        return {}
