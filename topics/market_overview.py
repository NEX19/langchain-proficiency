from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field, AnyUrl

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_perplexity import ChatPerplexity

from utils import create_chat


# TODO:
# 1) better serialization
# 2) better class devision


# TODO:
# Rewrite the whole thing


from typing import Any, Optional
from pydantic import BaseModel, Field, AnyUrl


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


class GeneralInformation(BaseModel):
    population: Optional[ValueWithSource] = Field(
        default=None,
        description=(
            "Total population (most recent official estimate). Provide as a numeric `val` inside ValueWithSource "
            "and cite the source."
        ),
    )
    capital_city: Optional[ValueWithSource] = Field(
        default=None,
        description="Name of the country's capital city. Provide as a string `val` inside ValueWithSource and cite the source.",
    )
    gdp: Optional[ValueWithSource] = Field(
        default=None,
        description=(
            "Nominal Gross Domestic Product. Prefer a numeric `val` and specify `unit` (e.g. 'USD') in ValueWithSource; "
            "include the year or date in `last_updated` if possible."
        ),
    )
    gdp_per_capita: Optional[ValueWithSource] = Field(
        default=None,
        description=(
            "GDP per capita (nominal). Prefer numeric `val`; include `unit` (e.g. 'USD') and `last_updated` (year/date) where available."
        ),
    )
    currency: Optional[ValueWithSource] = Field(
        default=None,
        description=(
            "Official currency of the market. Prefer the ISO 4217 three-letter code (e.g., 'EUR', 'USD') as the `val` and cite the source."
        ),
    )

    def fetch_info(llm: ChatPerplexity, market: str, product_category: str) -> GeneralInformation:
        structured_model = llm.with_structured_output(
            GeneralInformation
        )

        template = """You are a research assistant. Collect concise, factual data about the MARKET and PRODUCT_CATEGORY.
Return only a JSON object matching the schema indicated below.

Market: {market}
Product category: {product_category}

Instructions:
- For each field (population, capital_city, gdp, gdp_per_capita, currency) provide an object with at least "val" and "source".
- Use ISO dates (YYYY-MM-DD) for last_updated if applicable.
- If a value is unknown, omit that field rather than inventing data.
- Prefer authoritative sources and cite them in `source`.
- Keep numbers as numbers (no extra text).
        """
        prompt = PromptTemplate(
            input_variables=["market", "product_category"],
            template=template,
        )
        prompt_text = prompt.format(
            market=market,
            product_category=product_category
        )

        return structured_model.invoke(prompt_text)


class LegalAndTaxInfo(BaseModel):
    vat_rate: Optional[ValueWithSource] = None
    import_duties: Optional[ValueWithSource] = None
    tariffs: Optional[ValueWithSource] = None
    excise_taxes: Optional[ValueWithSource] = None
    industry_regulations: Optional[ValueWithSource] = None
    licensing_requirements: Optional[ValueWithSource] = None
    trade_agreements: Optional[ValueWithSource] = None
    legal_barriers: Optional[ValueWithSource] = None


class OverviewPydantic(BaseModel):
    """
    Top-level model
    """
    market: str
    product_category: str
    general: GeneralInformation = Field(default_factory=GeneralInformation)
    legal_and_tax: LegalAndTaxInfo = Field(default_factory=LegalAndTaxInfo)
    generated_at: str = Field(default_factory=lambda: datetime.now(
        timezone.utc).strftime('%m/%d/%Y'))

    def serialize(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)


def market_overview(market, product_category):
    """
    Creates market overview

    :return: serialized market overview
    """
    llm = create_chat()
    gen_info = GeneralInformation.fetch_info(llm, market, product_category)
    res = gen_info.model_dump(exclude_none=True)
    print(res)


if __name__ == "__main__":
    # res = market_overview()
    # print(res)
    pass
