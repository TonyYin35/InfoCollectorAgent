# Data Model

## Event (MVP)
Required output fields:
- id: string
- title: string
- city: string
- start_time?: ISO string
- end_time?: ISO string
- time_text?: string
- location_text?: string
- signup_hint?: string
- category: "cosplay_convention"|"pop_up"|"meetup_or_photowalk"|"other"
- source_urls: string[]  (>=1)
- primary_source_url: string
- evidence_snippets: { text: string, url: string }[]  (>=1, each <=200 chars)
- fetched_at: ISO string
- published_at?: ISO string
- confidence: "low"|"medium"|"high"

Recommended additional fields:
- tags?: string[]
- conflicts?: { field: "time"|"location"|"price"|"signup", values: string[], source_urls: string[] }[]

## Meta
- query_plan_summary: string
- sources_used: { source_id: string, urls_used: number, success: number, failed: number }[]
- fetched_at: ISO string
- warnings: { code: string, message: string, detail?: any }[]

## Warning codes (MVP)
- LOC_GEO_DENIED
- LOC_GEO_FAILED
- FETCH_TIMEOUT
- FETCH_BLOCKED
- EXTRACT_EMPTY
- EXTRACT_LOW_CONF
- CANDIDATE_INSUFFICIENT
- PROVIDER_DOWN

## QuerySpec (logging only, may be returned in meta.debug)
- user_location: { city: string }
- filters: { time_window_days: number, categories: string[], keyword?: string, limit: number }
- sources: { source_id: string, entry_url: string }[]
- time_generated: ISO
