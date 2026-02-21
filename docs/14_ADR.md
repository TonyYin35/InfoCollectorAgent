# ADR (Architecture Decision Records)

## ADR-001: Python backend + optional LangGraph
Decision: Use Python for API and pipeline. Use LangGraph for chat routing and future extensions.
Reason: Faster iteration, strong ecosystem for scraping and LLM orchestration.

## ADR-002: Fixed site entry recall for MVP
Decision: Do not use general search engine in MVP. Maintain 3-5 entry sites.
Reason: Predictability and lower cost; easier to debug extraction.

## ADR-003: Fetch strategy
Decision: Default requests; allow Playwright per-source fallback.
Reason: Keep MVP light but handle JS-rendered sources when needed.

## ADR-004: China Mainland only
Decision: Only Mainland cities in MVP.
Reason: Simplifies parsing and source selection.
