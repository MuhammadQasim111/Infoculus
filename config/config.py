import os
from dotenv import load_dotenv
from groq import AsyncGroq
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ChatCompletion

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env file")

if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY is missing in .env file")

# Initialize Groq client (sync for simplicity here)
groq_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"
