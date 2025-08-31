import asyncio
from typing import Any
from pydantic import BaseModel
import json

from agents.collector_agent import CollectorAgent

from models.market_overview import MarketOverview
from models.market_companies import CompanyList

from utils import save_json

if __name__ == "__main__":
    async def main():
        category = "machine learning"
        country = "Latvia"

        overview_agent = CollectorAgent(MarketOverview, country, category)
        companies_agent = CollectorAgent(CompanyList, country, category)

        results = await asyncio.gather(
            companies_agent.run(),
            overview_agent.run(),
            return_exceptions=True,
        )

        output = {}
        for topic, res in zip(["companies", "overview"], results):
            if isinstance(res, Exception):
                output[topic] = str(res)
            else:
                output[topic] = res.model_dump_json()

        save_json(output, f'{country}_{category}')

    asyncio.run(main())
