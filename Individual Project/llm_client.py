"""
Unified LLM client using Google Gemini API (OpenAI-compatible format).

Before use, set the GEMINI_API_KEY environment variable, or set API_KEY below.
Get your API key at https://aistudio.google.com/apikey
"""
import os
import time
from openai import OpenAI
from openai import InternalServerError, RateLimitError, APIConnectionError

# Read API key from environment variable, or set it directly below
API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Gemini OpenAI-compatible API endpoint
client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Default model; can be changed to gemini-1.5-flash, gemini-1.5-pro, etc. (more stable under load)
DEFAULT_MODEL = "gemini-3-flash-preview"

# Retry configuration for 503/429 errors
MAX_RETRIES = 5
INITIAL_BACKOFF = 2  # seconds


def call_llm(messages, model=None):
    """
    Call Gemini using OpenAI-compatible messages format.
    Automatically retries with exponential backoff on 503 (overload) and 429 (rate limit).

    Args:
        messages: OpenAI-format message list [{"role": "system/user/assistant", "content": "..."}]
        model: Model name; defaults to DEFAULT_MODEL

    Returns:
        str: The model's text response
    """
    if model is None:
        model = DEFAULT_MODEL

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except (InternalServerError, RateLimitError, APIConnectionError) as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                wait = INITIAL_BACKOFF * (2 ** attempt)
                err_type = "connection error" if isinstance(e, APIConnectionError) else "503/429"
                print(f"API temporarily unavailable ({err_type}), retrying in {wait:.0f}s ({attempt + 1}/{MAX_RETRIES})...")
                time.sleep(wait)
            else:
                raise
    raise last_error
