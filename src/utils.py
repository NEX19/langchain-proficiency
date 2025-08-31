from pydantic_ai import Agent, NativeOutput
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider

from pydantic import BaseModel, Field, AnyUrl
from typing import Any, Optional
from constants import OPENROUTER_API_KEY
import json


class ValueWithSource(BaseModel):
    """
    Represents a single metric value with source metadata.
    Minimal required fields: val, source.
    Optional: unit, source_url, last_updated, note, confidence.
    """
    val: Any = Field(
        ...,
        description=(
            "The metric value. Can be a number, string, or small structured object. "
            "For monetary amounts prefer a numeric value and set `unit` (e.g., 'USD')."
        ),
    )
    source: str = Field(
        ...,
        description=(
            "Short citation or source name for the value (e.g. 'World Bank', "
            "'National Statistics Office', or a short bibliographic string). Preferably include a URL "
            "in `source_url` when available."
        ),
    )
    note: Optional[str] = Field(
        default=None,
        description="Optional explanatory note or caveat about the value (e.g. estimation method, rounding).",
    )
    unit: Optional[str] = Field(
        default=None,
        description="Unit for the value (e.g. 'USD', '%', 'people'). Prefer standardized abbreviations.",
    )
    source_url: Optional[AnyUrl] = Field(
        default=None,
        description="URL pointing to the source document or page (useful for verification).",
    )
    last_updated: Optional[str] = Field(
        default=None,
        description="Date when the source/value was last updated. Use ISO format 'YYYY-MM-DD' when possible.",
    )
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Optional confidence score between 0.0 and 1.0 indicating estimated reliability of the value.",
    )


def create_agent(instructions: str, output_type: BaseModel, tools: list = []):
    model = OpenAIChatModel(
        'openai/gpt-4o',
        provider=OpenRouterProvider(
            api_key=OPENROUTER_API_KEY
        )
    )

    # TODO tools or toolsets?
    return Agent(model, instructions=instructions, output_type=output_type, tools=tools)


def load_markdown_prompt(prompt_path: str) -> str:
    """Load a markdown prompt file and return its content as a string."""
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    except Exception as e:
        raise RuntimeError(f"Error loading prompt file {prompt_path}: {e}")


def save_json(item: Any, save_as: str):
    filename = f'../test_runs/{save_as.lower().replace(' ', '_')}.json'
    if isinstance(item, BaseModel):
        item = item.model_dump_json()
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(item, f, ensure_ascii=False, indent=2)
