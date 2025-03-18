import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Try to get API keys from environment variables or Streamlit secrets
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("OPENAI_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY") or st.secrets.get("FIRECRAWL_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OpenRouter API key is not set in environment variables or Streamlit secrets")
if not FIRECRAWL_API_KEY:
    raise ValueError("Firecrawl API key is not set in environment variables or Streamlit secrets")

# OpenRouter configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_EXTRA_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://wateen.io",
    "X-Title": "WebToAgent"
}

# Model configuration
DEFAULT_MODEL = "openai/gpt-4o-mini"  # OpenRouter's model

# Firecrawl configuration
DEFAULT_MAX_URLS = 10
DEFAULT_USE_FULL_TEXT = False
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000
