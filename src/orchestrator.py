import asyncio
from typing import Any
from pydantic import BaseModel
import json

from agents.collector_agent import CollectorAgent
from agents.deep_think_agent import DeepThinkAgent

from models.market_overview import MarketOverview
from models.market_companies import CompanyList
from models.market_trends import MarketTrends

from utils import save_json

if __name__ == "__main__":
    async def main():
        category = "Beer"
        country = "Germany"
        agent_names = ["companies", "overview", "trends"]

        # TODO get rid of indexing
        overview_agent = CollectorAgent(
            MarketOverview, country, category, agent_name=agent_names[0])
        companies_agent = CollectorAgent(
            CompanyList, country, category, agent_name=agent_names[1])
        trends_agent = CollectorAgent(
            MarketTrends, country, category, agent_name=agent_names[2])

        results = await asyncio.gather(
            companies_agent.run(),
            overview_agent.run(),
            trends_agent.run(),
            return_exceptions=True
        )

        output = {}
        for name, res in zip(agent_names, results):
            if isinstance(res, Exception):
                output[name] = str(res)
            else:
                output[name] = res.model_dump_json()

        save_json(output, f'{country}_{category}')

        deep_think_agent = DeepThinkAgent(country, category, {})
        deep_think_output = await deep_think_agent.run()

        print(deep_think_output)
        filename = f'../test_runs/{country}_{category}.txt'.lower().replace(
            ' ', '_')
        with open(filename, 'w') as f:
            f.write(deep_think_output)

    asyncio.run(main())
