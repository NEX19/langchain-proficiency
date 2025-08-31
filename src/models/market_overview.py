from typing import Optional, ClassVar
from pydantic import BaseModel, Field
from utils import ValueWithSource


class MarketOverview(BaseModel):
    population: Optional[ValueWithSource] = Field(
        default=...,
        description="Total population (most recent official estimate). Provide numeric `val` and cite source."
    )
    capital_city: Optional[ValueWithSource] = Field(
        default=...,
        description="Name of the country's capital city. Provide string `val` and cite source."
    )
    gdp: Optional[ValueWithSource] = Field(
        default=...,
        description="Nominal Gross Domestic Product. Prefer numeric `val`, include `unit` (e.g. 'USD') and `last_updated` (year/date)."
    )
    gdp_per_capita: Optional[ValueWithSource] = Field(
        default=...,
        description="GDP per capita (nominal). Prefer numeric `val`, include `unit` and `last_updated`."
    )
    currency: Optional[ValueWithSource] = Field(
        default=...,
        description="Official currency (ISO 4217 three-letter code preferred, e.g., 'EUR', 'USD')."
    )
    vat_rate: Optional[ValueWithSource] = Field(
        default=...,
        description="Standard VAT/GST rate(s). Prefer numeric `val` as percent (e.g., 21). For multiple rates, provide a short structured string or list in `val` and cite source."
    )
    import_duties: Optional[ValueWithSource] = Field(
        default=...,
        description="High-level description or typical rates for import duties. Use numeric where appropriate; otherwise provide short descriptive `val`."
    )
    tariffs: Optional[ValueWithSource] = Field(
        default=...,
        description="Key tariff schedules or summary (e.g., average tariff %, notable sector tariffs). Prefer numeric when available; otherwise a concise string."
    )
    excise_taxes: Optional[ValueWithSource] = Field(
        default=...,
        description="Major excise taxes (e.g., on tobacco, alcohol, fuel). Summarize rates or basis of taxation."
    )
    industry_regulations: Optional[ValueWithSource] = Field(
        default=...,
        description="Short summary of industry-specific regulatory constraints relevant to foreign businesses (string `val`)."
    )
    licensing_requirements: Optional[ValueWithSource] = Field(
        default=...,
        description="Key licensing or registration requirements for operating in the market (string `val`)."
    )
    trade_agreements: Optional[ValueWithSource] = Field(
        default=...,
        description="Active major trade agreements affecting the country (string `val` listing agreements and role)."
    )
    legal_barriers: Optional[ValueWithSource] = Field(
        default=...,
        description="Major legal barriers to entry (e.g., foreign ownership limits, sectoral restrictions). Provide concise string `val` and sources."
    )

    retrieve_prompt_path: ClassVar[str] = "prompts/market_overview_retrieve_sys.md"
    consolidate_prompt_path: ClassVar[str] = "prompts/market_overview_consolidate_sys.md"
