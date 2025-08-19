from langchain.output_parsers import PydanticOutputParser
from langchain import PromptTemplate
from langchain_perplexity import ChatPerplexity


from typing import Dict
from constants import PPLX_API_KEY


def create_prompt_text(parser: PydanticOutputParser, template: str, input_variables: Dict[str, str]):
    prompt = PromptTemplate(
        input_variables=input_variables.keys(),
        template=template,
    )

    return prompt.format(
        **input_variables,
        format_instructions=parser.get_format_instructions(),
    )


def create_chat(model: str = "sonar-pro", temperature: float = 0.7):
    return ChatPerplexity(temperature=temperature, model=model, api_key=PPLX_API_KEY)
