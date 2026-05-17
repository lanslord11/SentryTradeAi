import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

# Retrieve the Ollama Cloud API key from your environment
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

def get_llm(temperature: float = 0.2):
    """Returns a configured Ollama Cloud LLM instance."""
    # Ensure you use an Ollama Cloud supported model name (e.g., "gpt-oss:120b")
    cloud_model = "gemma4:31b-cloud"
    
    return ChatOllama(
        model=cloud_model,
        temperature=temperature,
        # Point the host to Ollama's cloud API endpoint
        base_url="https://ollama.com",
        # Explicitly pass your bearer token in the headers
        headers={
            "Authorization": f"Bearer {OLLAMA_API_KEY}"
        }
    )
