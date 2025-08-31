from typing import Optional, ClassVar, Any
from pydantic import BaseModel, Field, model_serializer


class Company(BaseModel):
    name: str = Field(
        ...,
        description="Official company name (legal or commonly used trading name)."
    )
    linkedin_name: Optional[str] = Field(
        None,
        description="Company name as shown on LinkedIn (page title / official company name on LinkedIn)."
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
        description=(
            "Free-text notes about the record: data quality, sources, caveats "
            "(e.g. 'About text truncated; followers from LinkedIn; contact unverified')."
        )
    )


class CompanyList(BaseModel):
    company_list: list[Company] = Field([], description="List of companies")

    retrieve_prompt_path: ClassVar[str] = "prompts/market_companies_retrieve_sys.md"
    consolidate_prompt_path: ClassVar[str] = "prompts/market_companies_consolidate_sys.md"

    @model_serializer
    def ser_model(self) -> list[dict[str, Any]]:
        return [c.model_dump() for c in self.company_list]
