import streamlit as st
import asyncio
import threading
import queue

from src.config import (
    DEFAULT_MAX_URLS,
    DEFAULT_USE_FULL_TEXT,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_EXTRA_HEADERS
)
from src.llms_text import extract_website_content
from src.agents import extract_domain_knowledge, create_domain_agent, Runner
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent

# Configure OpenRouter client
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,  # Raw API key - Authorization header is in OPENROUTER_EXTRA_HEADERS
    base_url=OPENROUTER_BASE_URL
)

# Initialize session state
def init_session_state():
    if 'domain_agent' not in st.session_state:
        st.session_state.domain_agent = None
    if 'domain_knowledge' not in st.session_state:
        st.session_state.domain_knowledge = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'extraction_status' not in st.session_state:
        st.session_state.extraction_status = None
    if 'pending_response' not in st.session_state:
        st.session_state.pending_response = None

def run_app():
    # Initialize session state
    init_session_state()
    
    # Check if we have a pending response to add to the message history
    if st.session_state.pending_response is not None:
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.pending_response})
        st.session_state.pending_response = None
    
    # App title and description in main content area
    st.title("WebToAgent")
    st.subheader("Extract domain knowledge from any website and create specialized AI agents.")
    
    # Display welcome message using AI chat message component
    if not st.session_state.domain_agent:
        with st.chat_message("assistant"):
            st.markdown("👋 Welcome! Enter a website URL in the sidebar, and I'll transform it into an AI agent you can chat with.")
    
    # Form elements in sidebar
    st.sidebar.title("Create your agent")
    
    website_url = st.sidebar.text_input("Enter website URL", placeholder="https://example.com")
    
    max_pages = st.sidebar.slider("Maximum pages to analyze", 1, 25, DEFAULT_MAX_URLS, 
                         help="More pages means more comprehensive knowledge but longer processing time. Capped at 25 pages to respect rate limits.")
    
    use_full_text = st.sidebar.checkbox("Use comprehensive text extraction", value=DEFAULT_USE_FULL_TEXT,
                                help="Extract full contents of each page (may increase processing time)")
    
    submit_button = st.sidebar.button("Create agent", type="primary")
    
    # Process form submission
    if submit_button and website_url:
        st.session_state.extraction_status = "extracting"
        
        try:
            with st.spinner("Extracting website content with Firecrawl..."):
                content = extract_website_content(
                    url=website_url, 
                    max_urls=max_pages,
                    show_full_text=use_full_text
                )
                
                # Show content sample
                with st.expander("View extracted content sample"):
                    st.text(content['llmstxt'][:1000] + "...")
                
                # Process content to extract knowledge
                with st.spinner("Analyzing content and generating knowledge model..."):
                    domain_knowledge = asyncio.run(extract_domain_knowledge(
                        content['llmstxt'] if not use_full_text else content['llmsfulltxt'],
                        website_url
                    ))
                    
                    # Store in session state
                    st.session_state.domain_knowledge = domain_knowledge
                
                # Create specialized agent
                with st.spinner("Creating specialized agent..."):
                    domain_agent = create_domain_agent(domain_knowledge)
                    
                    # Store in session state
                    st.session_state.domain_agent = domain_agent
                    
                    st.session_state.extraction_status = "complete"
                    st.success("Agent created successfully! You can now chat with the agent.")
        
        except Exception as e:
            st.error(f"Error creating agent: {str(e)}")
            st.session_state.extraction_status = "failed"
    
    # Chat interface
    if st.session_state.domain_agent:
        display_chat_interface()

async def get_agent_response(agent, prompt: str) -> str:
    """Get response from agent with streaming support."""
    try:
        # Run the agent with streaming
        return await Runner.run_streamed(agent, prompt)
    except Exception as e:
        print(f"Error in streaming process: {str(e)}")
        # Fall back to standard response
        return await Runner.run(agent, prompt)

def display_chat_interface():
    """Display chat interface for interacting with the domain agent."""
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about the website..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                # Get response from agent
                response = asyncio.run(get_agent_response(st.session_state.domain_agent, prompt))
                
                # Display final response
                message_placeholder.markdown(response)
                
                # Add response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    run_app()
