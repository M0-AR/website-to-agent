import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY (for OpenRouter) is not set in environment variables or .env file")
OPENROUTER_API_KEY = os.getenv("OPENAI_API_KEY")  # Using OPENAI_API_KEY for OpenRouter

if not os.getenv("FIRECRAWL_API_KEY"):
    raise ValueError("FIRECRAWL_API_KEY is not set in environment variables or .env file")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# Default settings
DEFAULT_MAX_URLS = 10
DEFAULT_USE_FULL_TEXT = True
DEFAULT_MODEL = "openai/gpt-4o-mini"  # Using GPT-4O Mini via OpenRouter
DEFAULT_TEMPERATURE = 0.7  # OpenRouter recommended temperature
DEFAULT_MAX_TOKENS = 1000  # OpenRouter recommended max_tokens

# OpenRouter settings
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"  # Base URL from OpenRouter memory
OPENROUTER_EXTRA_HEADERS = {  # These will be passed as extra_headers in create()
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",  # Required by OpenRouter
    "HTTP-Referer": "https://wateen.io",  # Required for rankings
    "X-Title": "Website to Agent",  # Required for rankings
    "Content-Type": "application/json"  # Required by OpenRouter
}
