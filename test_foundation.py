"""
test_foundation.py — Phase 0 Foundation Test
=============================================
Run this BEFORE splitting work with your teammate.
Both machines must pass this test before anyone branches off.

What it tests:
  1. Settings load correctly from .env
  2. init_llm() runs without error
  3. call_llm() gets a real response from Ollama
  4. The response is valid JSON with an expected key

How to run:
    python test_foundation.py

Expected output (if everything is working):
    [1/4] Settings loaded       ✓  model=llama3.2
    [2/4] LLM client initialised ✓
    [3/4] LLM responded         ✓
    [4/4] JSON parsed correctly  ✓  greeting=Hello!
    
    ✅ Foundation test passed. Safe to split work.
"""

import asyncio
from core.config import settings
from core.llm_client import init_llm, call_llm


async def run_test():
    print("\nRunning foundation test...\n")

    # 1. Settings
    print(f"[1/4] Settings loaded        ✓  model={settings.model_name}")
    assert settings.model_name, "MODEL_NAME is empty — check your .env file"
    assert settings.ollama_base_url, "OLLAMA_BASE_URL is empty — check your .env file"

    # 2. Init LLM
    init_llm()
    print("[2/4] LLM client initialised  ✓")

    # 3. Call LLM
    system = "You are a helpful assistant. Always respond with valid JSON only. No explanation."
    user   = 'Respond with exactly this JSON: {"greeting": "Hello!"}'

    result = await call_llm(system, user)
    print("[3/4] LLM responded           ✓")

    # 4. Parse and assert
    assert "greeting" in result, (
        f"Expected 'greeting' key in response but got: {result}"
    )
    print(f"[4/4] JSON parsed correctly   ✓  greeting={result['greeting']}")

    print("\n✅ Foundation test passed. Safe to split work.\n")


if __name__ == "__main__":
    asyncio.run(run_test())