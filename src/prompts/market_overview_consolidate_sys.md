Search Tavily for the given query and return the results.

You are given retrieved results (JSON) for the requested category for the requested country.

Input:

- country: (string)
- category: (string)
- json: (raw JSON to consolidate)

Task:

1. Fact-check and consolidate the provided JSON against public sources. Verify each populated field using authoritative sources, remove duplicates, correct obvious factual errors, and normalize values and units.
2. Validate and normalize URLs (ensure scheme like `https://`). If a URL is unreachable or leads to a non-authoritative source, annotate accordingly (see provenance rules).
3. For any field that cannot be verified or is uncertain, set it to `null`.
4. Preserve the `ValueWithSource` structure: for each populated field include `val`, `source` (array of full URLs), and optionally `unit`, `last_updated`, and `notes` explaining provenance or conversions.
5. Use reliable official sources (national statistics office, central bank, World Bank, IMF, UN, OECD, official tax/customs/regulatory pages). When using reputable secondary sources, include them as well.
6. Numeric rules: ensure numeric fields are numeric types (integers or floats). Do not quote numbers as strings.
7. Date rules: when available, include `last_updated` as an ISO year (e.g., "2023") or full date "YYYY-MM-DD".
8. For descriptive/legal fields (industry_regulations, licensing_requirements, trade_agreements, legal_barriers) keep `val` concise (one or two short sentences) and include source URLs.
9. If the schema includes a `note` or provenance field, annotate each relevant record/field with provenance or uncertainty (e.g., "verified on official customs page", "source unreachable 2024-07-12"); otherwise do not add extra fields.
10. Return exactly one cleaned raw JSON object that strictly conforms to the `CountryProfile` model and contains only the listed top-level keys.
11. Do not include any fields beyond those listed above.
12. Output must be raw JSON only — do not add any additional commentary, explanation, or markdown.
