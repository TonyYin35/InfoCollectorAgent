# Test Plan (MVP)

## A. Location denied -> manual city -> search returns
Given: browser geolocation denied
When: city="杭州", time_window_days=7, categories=["cosplay_convention","pop_up"], limit=10
Then:
- returns ok=true
- events length is 1..10 (if <10 must include warning CANDIDATE_INSUFFICIENT)
- each event has primary_source_url + fetched_at + >=1 evidence_snippet

## B. Chat refetch ("只看周末")
Given: last_events exists for 杭州
When: /api/chat user_message="只看周末"
Then:
- action.type="refetch"
- updated_filters includes a weekend constraint (implementation-specific)
- new events returned

## C. Chat answer-only ("怎么报名")
Given: focus event exists
When: /api/chat user_message="怎么报名"
Then:
- action.type="answer_only"
- assistant_message cites evidence_snippets OR says insufficient evidence + link
- must not fabricate

## D. Dedupe sanity
Given: two sources reference same event
Then: clustered result includes merged source_urls and single primary_source_url
