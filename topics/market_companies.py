from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field
from utils import create_agent, MarketQuery
from loguru import logger
import json

from pydantic_ai import NativeOutput

# TODO
# 1. Switch from perplexity (it uses JSON output, doesn't have tools)
# 2. Add error return type for llm response
# 3. zip'ing llm responses is fucking stupid, think of something more reliable
# 4. Better naming
# 5. async requests

# suggestions
# 1. Maybe remove CompanyContact completely and concatenate all info inside one Company class?

# problems
# 1. CompanyContact finds not working linkedin links
# 2. CompanyInfo finds too few companies (3-5), need to expand


class CompanyInfo(BaseModel):
    name: str = Field(
        ...,
        description="Official company name (legal or commonly used trading name)."
    )
    headquarters: Optional[str] = Field(
        None,
        description="Headquarters location as listed on LinkedIn (city, region, country)."
    )
    size: Optional[str] = Field(
        None,
        description=(
            "Rough company size indicator. Examples: '10-50 employees', "
            "'5000+ employees', 'SME', 'regional', or an approximate revenue band."
        )
    )
    specialization: Optional[str] = Field(
        None,
        description=(
            "Short description of the company's focus or product/service categories "
            "(e.g. 'pharmaceutical distributor', 'grocery retailer — fresh produce')."
        )
    )
    company_size: Optional[str] = Field(
        None,
        description="Size range (e.g. '51-200 employees', '5000+'); use null if not listed."
    )
    note: Optional[str] = Field(
        None,
        description=(
            "Free-text notes about the record: data quality, sources, caveats"
        )
    )

    def retrieve(query: MarketQuery) -> List[CompanyInfo]:
        instructions = (
            "You are a focused, factual web researcher. "
            f"Search for companies operating in '{query.category}' industry in '{query.country}'. "
            "Be concise and evidence-based: rely on authoritative public sources (company websites, LinkedIn, official registries, reputable business directories). "
            "DO NOT invent or guess details. "
            "If a requested detail is not publicly available, leave it empty/null. "
            "Prioritize companies with significant operations in the specified country. "
            "Return ONLY the companies and strictly follow the external output schema provided by the caller — no extra commentary, methodology, or formatting beyond what the caller's schema expects."
        )
        output_type = NativeOutput(List[CompanyInfo])
        user_prompt = (
            "Find major distributors and retailers operating in "
            f"'{query.category}' industry in '{query.country}'. "
        )

        agent = create_agent(instructions=instructions,
                             output_type=output_type)
        result = agent.run_sync(user_prompt)
        return result.output


class CompanyContact(BaseModel):
    name: str = Field(
        ...,
        description="Company name as shown on LinkedIn (page title / official company name)."
    )
    linkedin_url: Optional[str] = Field(
        None,
        description="Full URL of the company's LinkedIn page (include scheme, e.g. 'https://www.linkedin.com/company/...')."
    )
    website: Optional[str] = Field(
        None,
        description="Website URL that LinkedIn lists on the company's profile (if present)."
    )
    email: Optional[str] = Field(
        None,
        description="Public business email address shown on the LinkedIn page (only include if explicitly listed)."
    )
    phone: Optional[str] = Field(
        None,
        description="Public phone number shown on the LinkedIn page (only include if explicitly listed)."
    )
    note: Optional[str] = Field(
        None,
        description="Concise provenance/data-quality hint (e.g. 'About text truncated; followers from LinkedIn; contact unverified')."
    )

    def retrieve(companies: List[CompanyInfo]) -> List[CompanyContact]:
        result: List[CompanyContact] = []
        instructions = (
            "You are a research assistant specializing in extracting verified business contact information."
            "Task:"
            "- Given a specific company name (from the user prompt), find its official LinkedIn page and extract structured information."
            "- Fill only the fields that can be verified from the LinkedIn company profile or other official sources (company website linked from LinkedIn, official registries, reputable directories)."
            "- Do NOT invent or guess. If a field cannot be confirmed, set it to null."
            "- For phone/email: include ONLY if they are explicitly listed publicly on LinkedIn or the official company website. Never infer or fabricate."
            "- For About text, company size, headquarters, specialties, and founded year: use LinkedIn data if available."
            "- For note: briefly summarize provenance and data quality (≤200 chars)."
            "Output must conform strictly to the provided Pydantic schema."
        )

        output_type = NativeOutput(CompanyContact)
        agent = create_agent(instructions=instructions,
                             output_type=output_type)

        for c in companies:
            user_prompt = f"Find LinkedIn company profile and contact info for: {c.name}, {c.headquarters}"
            res = agent.run_sync(user_prompt)
            result.append(res.output)
            logger.info(
                f'Company: {c.name}, {c.headquarters}\nUsage:{res.usage()}')

        return result


class CompanyWrap(BaseModel):
    # dummy wrapper class
    contact: CompanyContact
    info: CompanyInfo


class MarketCompanies(BaseModel):
    query: MarketQuery = Field(None)
    companies: List[CompanyWrap] = Field([])

    def retrieve(self, query: MarketQuery):
        self.query = query
        infos = CompanyInfo.retrieve(query)
        logger.info(len(infos))
        contacts = CompanyContact.retrieve(infos)

        for (info, contact) in zip(infos, contacts):
            company = CompanyWrap(info=info, contact=contact)
            self.companies.append(company)

    def to_json(self, save_file=True):
        js = self.model_dump()
        if save_file:
            file_name = f'test_runs/{self.query.country.replace(" ", "_")}_{self.query.category.replace(" ", "_")}.json'
            with open(file_name, 'w') as f:
                json.dump(js, f)

        return js
