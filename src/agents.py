from datetime import datetime
from typing import List

from src.models import Concept, Terminology, Insight, DomainKnowledge
from src.config import DEFAULT_MODEL
from src.openrouter_agent import Agent, Runner, ModelSettings

async def extract_domain_knowledge(content: str, url: str) -> DomainKnowledge:
    """
    Extract structured domain knowledge from website content.
    
    Args:
        content: The extracted website content (llmstxt or llmsfulltxt)
        url: Source URL for reference
        
    Returns:
        Structured DomainKnowledge object
    """
    # Create knowledge extraction agent
    knowledge_extractor = Agent(
        name="Knowledge Extractor",
        instructions="""You are a precise knowledge extraction system. Your task is to analyze website content and output ONLY a JSON object that matches this exact schema:

{
    "core_concepts": [
        {
            "name": "string",
            "description": "string",
            "related_concepts": ["string"],
            "importance_score": float  // 0.0-1.0
        }
    ],
    "terminology": [
        {
            "term": "string",
            "definition": "string",
            "context": "string or null",
            "examples": ["string"]
        }
    ],
    "key_insights": [
        {
            "content": "string",
            "topics": ["string"],
            "confidence": float  // 0.0-1.0
        }
    ],
    "source_url": "string",
    "extraction_timestamp": "string"
}

CRITICAL REQUIREMENTS:
1. Output ONLY valid JSON - no markdown, no explanations
2. Every field must match the schema exactly
3. All strings must be properly escaped
4. All arrays must be properly formatted
5. All floats must be between 0.0 and 1.0
6. Never include line breaks within strings

Example values:
- importance_score: 0.8 for primary concepts, 0.4 for secondary ones
- confidence: 0.9 for explicitly stated insights, 0.5 for inferred ones
""",
        output_type=DomainKnowledge,
        model=DEFAULT_MODEL,
        model_settings=ModelSettings(
            temperature=0.7,  # Match OpenRouter recommended temperature
            max_tokens=1000,  # Match OpenRouter recommended max_tokens
        )
    )
    
    # Run the extraction agent
    result = await Runner.run(
        knowledge_extractor, 
        f"""Extract domain knowledge from this website content and output ONLY valid JSON:

Content:
{content}

Source: {url}

Remember: Output ONLY the JSON object - no explanations or other text."""
    )
    
    # Return the structured knowledge
    domain_knowledge = result
    domain_knowledge.source_url = url
    domain_knowledge.extraction_timestamp = datetime.now().isoformat()
    
    return domain_knowledge

def create_domain_agent(domain_knowledge: DomainKnowledge) -> Agent:
    """
    Create a specialized agent based on extracted domain knowledge.
    
    Args:
        domain_knowledge: Structured domain knowledge
        
    Returns:
        Configured OpenAI Agent with domain expertise
    """
    # Generate agent instructions from domain knowledge
    instructions = f"""You are an expert on {domain_knowledge.core_concepts[0].name if domain_knowledge.core_concepts else "this domain"} 
    with specialized knowledge based on content from {domain_knowledge.source_url}.
    
    DOMAIN CONCEPTS:
    {_format_concepts(domain_knowledge.core_concepts)}
    
    TERMINOLOGY:
    {_format_terminology(domain_knowledge.terminology)}
    
    KEY INSIGHTS:
    {_format_insights(domain_knowledge.key_insights)}
    
    When answering questions:
    1. Draw on this specialized knowledge first
    2. Clearly indicate when you're using information from the source material
    3. If asked something outside this domain knowledge, acknowledge the limitations
    4. Structure complex answers with headings and bullet points for clarity
    5. Refer to the source URL when appropriate
    
    Provide accurate, insightful responses based on this domain knowledge.
    """
    
    # Create domain-specific agent
    domain_agent = Agent(
        name=f"Domain Expert: {domain_knowledge.source_url}",
        instructions=instructions,
        model=DEFAULT_MODEL,
        model_settings=ModelSettings(
            temperature=0.7,  # Match OpenRouter recommended temperature
            max_tokens=1000,  # Match OpenRouter recommended max_tokens
        )
    )
    
    return domain_agent

def _format_concepts(concepts: List[Concept]) -> str:
    """Format concepts for agent instructions."""
    formatted = ""
    for concept in concepts:
        formatted += f"- {concept.name}: {concept.description}\n"
        if concept.related_concepts:
            formatted += f"  Related: {', '.join(concept.related_concepts)}\n"
    return formatted

def _format_terminology(terminology: List[Terminology]) -> str:
    """Format terminology for agent instructions."""
    formatted = ""
    for term_info in terminology:
        formatted += f"- {term_info.term}: {term_info.definition}\n"
        if term_info.examples:
            formatted += f"  Examples: {'; '.join(term_info.examples)}\n"
    return formatted

def _format_insights(insights: List[Insight]) -> str:
    """Format insights for agent instructions."""
    formatted = ""
    for insight in insights:
        formatted += f"- {insight.content}\n"
    return formatted
