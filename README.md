# WebToAgent

WebToAgent is a Streamlit application that extracts domain knowledge from websites and creates specialized AI agents capable of answering questions about that domain. By leveraging web crawling and advanced language models, WebToAgent transforms website content into interactive, conversational agents.

> This project is a fork of [firecrawl-app-examples](https://github.com/mendableai/firecrawl-app-examples) with modifications to use OpenRouter API instead of OpenAI directly.

 **[Live Demo](https://website-to-agent.streamlit.app/)**

![WebToAgent Screenshot](https://placeholder-for-screenshot.png)

## Features

- **Website content extraction**: Crawl websites using Firecrawl to extract relevant content
- **Knowledge model generation**: Process extracted content to build domain-specific knowledge models
- **AI agent creation**: Create conversational agents specialized in the crawled domain
- **Interactive chat interface**: Engage with your domain agent through a real-time chat interface
- **Streaming responses**: Get real-time streaming responses from the agent as it generates them
- **OpenRouter integration**: Uses OpenRouter API for flexible access to various language models

## Prerequisites

Before installing WebToAgent, make sure you have:

- Python 3.9+ installed
- Pip (Python package installer)
- Access to Firecrawl API credentials
- Access to OpenRouter API credentials

## Installation

1. Clone the repository:

   ```bash
   git clone <your-repository-url>
   cd website-to-agent
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your API credentials (see Configuration section)

## Configuration

### Local Development

1. Create a `.env` file in the project root with your API credentials:

   ```bash
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

2. You can customize default settings in the `src/config.py` file, including:
   - `DEFAULT_MAX_URLS`: Maximum number of URLs to crawl (default: 10)
   - `DEFAULT_USE_FULL_TEXT`: Whether to use comprehensive text extraction (default: False)
   - `DEFAULT_MODEL`: OpenRouter model to use (default: openai/gpt-4o-mini)

### Streamlit Cloud Deployment

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app" and select your forked repository
4. Select `app.py` as the main file
5. **Important**: Add your API keys in Streamlit Cloud:
   - Go to "Advanced settings" 
   - Under "Secrets", add the following in TOML format:
     ```toml
     OPENROUTER_API_KEY = "your_openrouter_api_key"
     FIRECRAWL_API_KEY = "your_firecrawl_api_key"
     ```
6. Deploy your app

**Never commit API keys to your repository. Always use environment variables or Streamlit secrets.**

## Usage

1. Start the Streamlit application:

   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Enter a website URL in the sidebar

4. Configure crawling options:
   - Adjust the maximum pages to analyze
   - Toggle comprehensive text extraction

5. Click "Create agent" to start the process

6. Once the agent is created, you can ask questions about the website's domain in the chat interface

## How it works

WebToAgent operates in three main phases:

1. **Content extraction**: Using Firecrawl, the application crawls the specified website, gathering content from pages within the domain. The depth and breadth of crawling can be adjusted through the UI.

2. **Knowledge model creation**: The extracted content is processed to build a domain-specific knowledge representation. This phase identifies key concepts, relationships, and information from the website.

3. **Agent creation**: The domain knowledge is used to create a specialized AI agent. The agent uses OpenRouter to access language models and provide conversational responses to questions about the website's domain.

## OpenRouter Integration

This version of WebToAgent uses OpenRouter API for language model access, which offers several advantages:

1. **Model flexibility**: Access to various language models through a single API
2. **Cost optimization**: Choose models based on your performance and budget requirements
3. **Streaming support**: Real-time streaming responses for better user experience

The default configuration uses the `openai/gpt-4o-mini` model, which offers:
- 128K context window
- Competitive pricing ($0.15/M input tokens, $0.6/M output tokens)
- High-quality responses for domain-specific tasks

You can modify the model in `src/config.py` to use any model supported by OpenRouter.

## Troubleshooting

### Common issues

- **API key errors**: Make sure your API keys are properly set in the environment variables or Streamlit secrets. Never expose your API keys in the code.

- **Streaming responses disappearing**: If streaming responses disappear when submitting a new message, restart the application. The app utilizes a mechanism to maintain streaming state across Streamlit reruns.

- **API rate limiting**: If you encounter rate limit errors, reduce the maximum pages to analyze or add delays between requests in the configuration.

- **Memory issues**: For large websites, consider increasing the available memory for the Python process or reducing the scope of crawling.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## Acknowledgments

- Original repository: [firecrawl-app-examples](https://github.com/mendableai/firecrawl-app-examples)
- [Firecrawl](https://firecrawl.dev) for web crawling capabilities
- [OpenRouter](https://openrouter.ai) for language model access
- [Streamlit](https://streamlit.io) for the web application framework
