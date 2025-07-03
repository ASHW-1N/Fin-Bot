import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_response_from_llm(prompt: str) -> str:
    """
    Uses Groq API with LLaMA3-70B to generate a natural language response from the given prompt.
    """
    if not GROQ_API_KEY:
        return "❌ Missing GROQ_API_KEY in .env"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a SEBI-registered senior market analyst with 20+ years of experience. Give deep, data-backed, technical analysis using NSE data. No fluff."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 800
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"❌ Groq LLM Error: {e}"
