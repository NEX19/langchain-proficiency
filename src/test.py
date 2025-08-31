from utils import create_agent
from tools.web_search import web_search

tools = [web_search()]

agent = create_agent(
    "Search Tavily for the given query and return the results.", str, tools)

result = agent.run_sync(
    'Tell me the top news in the GenAI world, give me url links.')
print(result.output)
