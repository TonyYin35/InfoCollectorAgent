# Architecture (Python + optional LangGraph)

## Scope
- China Mainland cities only
- City-level "nearby" (string match on city/area keywords)
- Fixed site entry recall (no general search engine in MVP)
- On-demand crawling per user request (refresh triggers pipeline)

## Components
1) Web Frontend
- Shows city, filters, Top 10 event cards, evidence expansion, chat box.
- Calls POST /api/search on load and on filter changes.
- Calls POST /api/chat for chat interactions.

2) API Backend (Python)
- /api/search: runs retrieval pipeline and returns events + meta
- /api/chat: runs LangGraph router, may refetch or answer only

3) Retrieval Pipeline (pure python services)
- QueryBuilder: build query plan from location+filters
- Provider: returns candidate URLs from fixed sources (SOURCES.yaml)
- Fetcher: fetch HTML/text (requests by default; optional Playwright fallback per policy)
- Extractor: parse Event fields + evidence snippets
- Normalizer: normalize city/time fields when possible
- Dedupe/Cluster: merge duplicates
- Ranker: rule-based scoring
- EvidenceBuilder: ensures each Event has >=1 evidence snippet
- Logger: emits QuerySpec, sources_used, counts, failure reasons

## Suggested repo layout
apps/
  api/
    main.py
    routes/
    services/
    schemas/
    config/
  web/ (optional)
packages/
  shared/
docs/
