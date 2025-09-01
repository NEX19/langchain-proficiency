from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from typing import Type, Optional, Any
import asyncio

from utils import create_agent, load_markdown_prompt
from tools.web_search import web_search


class CollectorAgent:
    def __init__(self,
                 data_model_cls: Type[BaseModel],
                 country: str,
                 category: str,
                 agent_name: str = "agent_name"):
        self.data_model_cls = data_model_cls
        self.country = country
        self.category = category

        self._agent_name = agent_name

        retrieve_sys = load_markdown_prompt(
            data_model_cls.retrieve_prompt_path)
        consolidate_sys = load_markdown_prompt(
            data_model_cls.consolidate_prompt_path)

        tools = [web_search()]

        self.retrieve_agent = create_agent(retrieve_sys, data_model_cls, tools)
        self.consolidate_agent = create_agent(
            consolidate_sys, data_model_cls, tools)

        self._retrieve_user_prompt = (
            "Find factual, public information about '{category}' in '{country}'. "
            "Search reputable public sources and return structured results that conform to the "
            "system schema (the system prompt provides the exact object schema). "
            "Return a JSON array with up to 10 objects that match the schema. "
            "For any field that is not available, set it to null. "
            "If the schema defines a 'note' or provenance field, use it to record uncertainty or source hints; "
            "otherwise do not add extra fields. "
            "**Return only the JSON array** — no explanatory text or commentary."
        )

        self._consolidate_user_prompt = (
            "You are given retrieved results (JSON) for '{category}' in '{country}':\n\n"
            "{json}\n\n"
            "Task: Fact-check and consolidate these records against public sources. "
            "Remove duplicates, correct obvious factual errors, validate and normalize URLs (include scheme), "
            "and mark unverifiable or uncertain fields as null. If the schema includes a 'note' or provenance field, "
            "annotate each record with provenance or uncertainty (for example: 'verified on LinkedIn', 'website unreachable'). "
            "Return a cleaned JSON array of up to 10 objects that strictly conform to the system schema. "
            "**Return only the JSON array** — do not add any additional commentary or explanation."
        )

    async def _retrieve(self) -> Any:
        print(f"starting retrieve for {self._agent_name}")

        prompt = self._retrieve_user_prompt.format(
            category=self.category, country=self.country)
        res = await self.retrieve_agent.run(prompt)

        return res.output

    async def _consolidate(self, raw_data: Any) -> Any:
        print(f"starting consolidate for {self._agent_name}")

        # TODO better type checks between nodes pass

        prompt = self._consolidate_user_prompt.format(
            category=self.category, country=self.country, json=raw_data.model_dump_json())
        res = await self.consolidate_agent.run(prompt)
        return res.output

    async def run(self) -> Any:
        raw = await self._retrieve()
        structured = await self._consolidate(raw)
        return structured
