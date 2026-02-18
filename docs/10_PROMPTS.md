# Prompts (MVP)

## Intent classification (ParseIntentNode)
System:
你是一个路由器。只能输出 JSON。不要解释。

User input:
- user_message: ...
- current filters: ...
- city: ...
Task:
输出:
{
  "type": "refetch"|"answer_only",
  "updated_filters": {... optional ...},
  "focus_event_id": "... optional ..."
}

Rules:
- If message changes time/location/category/limit => refetch.
- Else answer_only.
- Do not invent event details.

## Extraction fallback (Extractor)
Given page text excerpt (<=2000 chars), extract:
title, time_text, location_text, signup_hint, evidence_snippets (<=200 chars each)
If not found, output empty fields, but keep at least one evidence snippet if any useful text exists.
