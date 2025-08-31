from constants import TAVILY_API_KEY
from pydantic_ai.common_tools.tavily import tavily_search_tool


def web_search():
    """
        Web search tool
        Uses default tavily web_search for now, maybe will improve in future
    """
    return tavily_search_tool(TAVILY_API_KEY)
