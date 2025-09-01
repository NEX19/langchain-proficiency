import json
from typing import Any

# pydantic_ai Agent/RunContext are referenced only to match your environment
from pydantic_ai import Agent
from utils import create_agent, load_markdown_prompt
from tools.web_search import web_search


class DeepThinkAgent:
    """
    Minimal DeepThinkAgent:
    - country: str
    - category: str
    - json_input: Any (raw records / collector output)
    - Uses web_search() tool
    - Returns an unstructured (plain text) analysis (no JSON/schema)
    """

    def __init__(self,
                 country: str,
                 category: str,
                 json_input: Any,
                 agent_name: str = "deep_think_agent"):
        self.country = country
        self.category = category
        self.json_input = json_input
        self._agent_name = agent_name

        self._system_prompt = load_markdown_prompt(
            "prompts/deep_think_sys.md")
        self._user_prompt_template = load_markdown_prompt(
            "prompts/deep_think_user.md")

        self.tools = [web_search()]

        self.agent: Agent = create_agent(self._system_prompt, tools=self.tools)

    async def run(self) -> str:
        """
        Run the DeepThinkAgent: sends a prompt which includes the country, category and the json_input.
        Returns the agent's unstructured text output (res.output).
        """
        try:
            json_input_text = json.dumps(
                self.json_input, ensure_ascii=False, indent=2)
        except (TypeError, ValueError):
            json_input_text = str(self.json_input)

        user_prompt = self._user_prompt_template.format(
            country=self.country,
            category=self.category,
            json_input=json_input_text
        )

        res = await self.agent.run(user_prompt)

        return res.output
