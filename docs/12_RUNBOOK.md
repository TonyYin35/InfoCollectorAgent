# Runbook

## Prerequisites
- Python 3.11+
- (optional) Playwright installed + browsers downloaded

## Env vars
- CACHE_TTL_SECONDS=900
- FETCH_TIMEOUT_MS=8000
- MAX_CANDIDATE_URLS=30
- MAX_DOMAIN_CONCURRENCY=2
- LLM_ENABLED=false|true
- OPENAI_API_KEY=... (if LLM enabled)

## Local run
1) install deps
2) start api
3) open web
4) sanity check endpoints:
- POST /api/search
- POST /api/chat

## Common failures
- empty results => check SOURCES.yaml entry_urls and city placeholder
- blocked => switch that source to playwright or reduce frequency
- extraction poor => adjust site extractor or category map keywords
