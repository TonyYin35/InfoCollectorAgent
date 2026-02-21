# LangGraph Chat Router (MVP)

## Purpose
Decide whether user message triggers:
- refetch (update filters/location/limit then call /api/search internally)
- answer_only (answer based on last_events evidence)

## Graph nodes
1) ParseIntentNode
- input: user_message, current_state
- output: intent {type, updated_filters?, focus_event_id?}

2) If refetch -> SearchNode
- runs pipeline with updated filters
- returns events + meta

3) If answer_only -> AnswerNode
- can only use current_state.last_events evidence
- MUST quote or reference evidence snippets, or say insufficient evidence + primary_source_url

## Intent rules (MVP)
refetch triggers:
- time terms: 今天/本周/周末/未来7天/未来30天
- location terms: city/区/地标关键词（string match）
- category terms: 漫展/快闪/外拍/同好会 -> map to category
- limit terms: 5/10/20条

answer_only triggers:
- 报名/买票/几点/地点/费用/交通/官网/主办

## Tooling
- optional LLM usage allowed ONLY in ParseIntentNode (classification) and Extractor fallback.
- AnswerNode must be deterministic and evidence-bound.
