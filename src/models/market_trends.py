from typing import Optional, List, ClassVar
from pydantic import BaseModel, Field
from utils import ValueWithSource


class MarketTrends(BaseModel):
    """
    Market Trends and Data schema:
    - Use ValueWithSource for any field where a numeric/text value + source attribution is expected.
    - For lists, each item is a ValueWithSource so every element can carry its own source.
    """

    market_size_latest: Optional[ValueWithSource] = Field(
        default=...,
        description=(
            "Latest market size (volume or value). Prefer numeric `val` with `unit` (e.g. 'USD', 'units') "
            "and `last_updated` (date/year). If both value and volume exist, include the most relevant and note the other in `notes`."
        )
    )
    market_size_breakdown: Optional[List[ValueWithSource]] = Field(
        default=...,
        description=(
            "Breakdown of market size by segment/channel/region (list of ValueWithSource). "
            "Each item should indicate the segment name and its `val` (share, value or volume) and source."
        )
    )
    historical_trends: Optional[List[ValueWithSource]] = Field(
        default=...,
        description=(
            "Historical growth / trend data (list). Each ValueWithSource should contain a single-period datapoint "
            "such as {'val': 5.2, 'unit': '%', 'period': '2019-2024 CAGR', 'note': 'or year-specific value' } and cite source."
        )
    )
    forecast_trends: Optional[List[ValueWithSource]] = Field(
        default=...,
        description=(
            "Forecasted growth / trend data (list). Prefer structured items indicating forecast period, expected CAGR or yearly values, "
            "and the source/provider of the forecast."
        )
    )
    cagr_summary: Optional[ValueWithSource] = Field(
        default=...,
        description="Consolidated CAGR(s) where applicable (e.g., '2024-2029 CAGR = 6.1%'). Provide period and source."
    )
    consumer_behavior_insights: Optional[ValueWithSource] = Field(
        default=...,
        description=(
            "Key consumer behavior insights (text `val` plus optional metric subfields). Examples: purchase frequency, "
            "average basket value, preferred channels, key decision factors. Cite consumer surveys, panel data or studies."
        )
    )
    distribution_channel_shares: Optional[List[ValueWithSource]] = Field(
        default=...,
        description=(
            "Share by distribution channel (e.g., 'online', 'modern trade', 'traditional retail'). Each entry should include channel name, share (percent/value) and source."
        )
    )
    pricing_trends_and_elasticity: Optional[ValueWithSource] = Field(
        default=...,
        description=(
            "High-level pricing trends and observed price elasticity (text or numbers). Include notable price points, trend direction, "
            "and source (retailer data, market reports)."
        )
    )
    import_export_data: Optional[ValueWithSource] = Field(
        default=...,
        description=(
            "Imports/exports relevant to the category. Prefer structured `val` (e.g., volumes/values and major trading partners) "
            "and include customs or trade database source and last-updated date."
        )
    )
    seasonality_and_cyclicality: Optional[ValueWithSource] = Field(
        default=...,
        description="Notes on seasonality or cyclical demand patterns (months/quarters with peaks/troughs) and source."
    )
    major_competitors_and_shares: Optional[List[ValueWithSource]] = Field(
        default=...,
        description=(
            "List of major players and (where available) market shares. Each ValueWithSource should include the company name in `val` "
            "and a numeric share or qualitative position in `note`, plus source."
        )
    )
    key_challenges: Optional[List[ValueWithSource]] = Field(
        default=...,
        description="Top challenges facing the category (regulatory, supply chain, demand-side, competitive). Each item should cite a source."
    )
    key_opportunities: Optional[List[ValueWithSource]] = Field(
        default=...,
        description="Top opportunities (new channels, underserved segments, product adjacencies). Each item should cite a source where possible."
    )
    analyst_notes: Optional[ValueWithSource] = Field(
        default=...,
        description="Free-text analyst notes or caveats about data quality, comparability, or important assumptions; include source if applicable."
    )

    retrieve_prompt_path: ClassVar[str] = "prompts/market_trends_retrieve_sys.md"
    consolidate_prompt_path: ClassVar[str] = "prompts/market_trends_consolidate_sys.md"
