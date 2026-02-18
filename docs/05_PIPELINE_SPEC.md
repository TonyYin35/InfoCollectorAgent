# Retrieval Pipeline Spec (MVP)

## Pipeline stages
1) BuildPlan(location, filters) -> Plan
2) Provider(plan) -> candidate_urls[]
3) Fetch(candidate_urls) -> pages[{url, html/text, status, error?}]
4) Extract(pages) -> extracted_events[]
5) Normalize(extracted_events) -> normalized_events[]
6) Cluster/Dedupe(normalized_events) -> clustered_events[]
7) Rank(clustered_events, filters) -> top_events[]
8) EvidenceCheck(top_events) -> ensure each has >=1 evidence snippet
9) Return(events, meta)

## Contracts
Provider:
input: Plan
output: [{url, source_id, source_type, hint_category?}]

Fetcher:
- default requests
- follow docs/09_FETCH_POLICY.md for Playwright fallback

Extractor output must include:
- title (or fallback from page title)
- evidence_snippets (>=1 if any content exists)

Dedupe rule (MVP):
- same URL => same item
- high title similarity + near time clue + near location clue => merge
- merged keeps multiple source_urls; choose primary by (source trust + completeness)

Rank rule (MVP):
score = time_match + city_match + source_trust + completeness
