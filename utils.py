from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from pydantic import BaseModel
from typing import Any
from constants import PPLX_API_KEY


class MarketQuery(BaseModel):
    country: str
    category: str


def create_agent(instructions: str, output_type: Any):
    model = OpenAIModel(
        'sonar-pro',
        provider=OpenAIProvider(
            base_url='https://api.perplexity.ai',
            api_key=PPLX_API_KEY,
        )
    )
    return Agent(model, instructions=instructions, output_type=output_type)
