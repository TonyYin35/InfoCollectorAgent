# Fetch Policy (MVP)

Default: requests + HTML parsing.

Enable Playwright fallback per-source when:
- consecutive EXTRACT_EMPTY >= 3
- or FETCH_BLOCKED rate > 30% for that source
- or site known to be JS-rendered (manual flag in SOURCES.yaml)

Per-source fetch_policy.mode:
- requests
- playwright

Hard limits:
- max_candidate_urls_per_search: 30
- max_domain_concurrency: 2
- cache_ttl_minutes: 10-30

Robots / login walls:
- If requires login or explicit block, skip and emit warning FETCH_BLOCKED.
