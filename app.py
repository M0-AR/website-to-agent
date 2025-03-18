import streamlit as st
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from src.ui import run_app

# Set page config
st.set_page_config(
    page_title="KnowledgeForge",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Run the application
if __name__ == "__main__":
    run_app()