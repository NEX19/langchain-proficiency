from dotenv import load_dotenv
import os

load_dotenv()

PPLX_API_KEY = os.getenv("PPLX_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
