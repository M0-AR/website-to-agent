from typing import Any, Dict, Optional, Type, TypeVar
from pydantic import BaseModel
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion import ChatCompletionMessage

from src.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_EXTRA_HEADERS,
    DEFAULT_MODEL
)

T = TypeVar('T', bound=BaseModel)

class ModelSettings:
    def __init__(self, temperature: float = 0.7, max_tokens: int = 1000):  # Match OpenRouter defaults
        self.temperature = temperature
        self.max_tokens = max_tokens

class Agent:
    def __init__(
        self,
        name: str,
        instructions: str,
        model: str = DEFAULT_MODEL,
        output_type: Optional[Type[T]] = None,
        model_settings: Optional[ModelSettings] = None
    ):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.output_type = output_type
        self.model_settings = model_settings or ModelSettings()
        
        # Create OpenRouter client
        self.client = AsyncOpenAI(
            api_key=OPENROUTER_API_KEY,  # Raw API key - Authorization header is in OPENROUTER_EXTRA_HEADERS
            base_url=OPENROUTER_BASE_URL  # Base URL from memory
        )

    async def run(self, prompt: str) -> Any:
        """Run the agent with the given prompt."""
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.model_settings.temperature,
            max_tokens=self.model_settings.max_tokens,
            stream=False,
            extra_headers=OPENROUTER_EXTRA_HEADERS
        )
        
        result = response.choices[0].message.content
        
        # Parse result if output type is specified
        if self.output_type and result:
            try:
                return self.output_type.model_validate_json(result)
            except Exception as e:
                raise ValueError(f"Failed to parse response as {self.output_type.__name__}: {e}")
        
        return result

class Runner:
    @staticmethod
    async def run(agent: Agent, prompt: str) -> Any:
        """Run an agent with the given prompt."""
        return await agent.run(prompt)

    @staticmethod
    async def run_streamed(agent: Agent, prompt: str) -> str:
        """Run an agent with streaming enabled and return the final response."""
        messages = [
            {"role": "system", "content": agent.instructions},
            {"role": "user", "content": prompt}
        ]
        
        final_response = []
        
        async with agent.client.chat.completions.create(
            model=agent.model,
            messages=messages,
            temperature=agent.model_settings.temperature,
            max_tokens=agent.model_settings.max_tokens,
            stream=True,
            extra_headers=OPENROUTER_EXTRA_HEADERS
        ) as stream:
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    final_response.append(chunk.choices[0].delta.content)
        
        return "".join(final_response)
