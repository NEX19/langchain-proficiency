Context:

- Country: {country}
- Category: {category}
- Retrieved records (provided below):  
  {json_input}

(Examples: risk tolerance, target return, investment size, timeline — include if you have them.)

Task:
Using the retrieved records and, if needed, targeted external searches (use available tools such as web_search), decide whether the client should invest in this category in this country. Produce a clear, actionable, human-readable analysis that follows this structure exactly:

1. Executive decision (1–2 sentences)
   - One-line decision: Invest / Do NOT Invest / Conditional (include investment horizon: short/medium/long).
2. Confidence (0–100%) and brief justification for that confidence.
3. Top 4 supporting facts (each as a short bullet). For any fact checked or supplemented with external search, include an inline citation (URL or tool evidence).
4. Major risks and mitigations (1–3 bullets).
5. Critical unknowns and how to resolve them (concrete queries/actions to run — e.g., “check import tariffs X; query regulator Y for licensing timeline”).
6. 1–3 recommended next actions (due diligence, monitoring metrics, or go/no-go triggers).
7. Key assumptions used to reach your recommendation (explicit and short).

Formatting rules:

- Return plain text only (no JSON). Use short bullets and numbered lists.
- If you perform external searches, cite sources inline for each claim that relied on them.
- If the input records are insufficient to make a recommendation, state this clearly and provide the minimum required data/queries that would allow a confident decision.
- If your recommendation is conditional, specify the exact conditions that would flip the decision.

Now: analyze the records, perform any targeted searches you need, and produce the decision and supporting analysis described above.
