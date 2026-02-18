# API Spec (MVP)

## Envelope
Response always:
- ok: boolean
- data?: object
- error?: { code: string, message: string }

## POST /api/search
Request:
{
  "location": { "city": "杭州" },
  "filters": { "time_window_days": 7, "categories": ["cosplay_convention","pop_up"], "keyword": "", "limit": 10 }
}

Response (ok):
{
  "ok": true,
  "data": { "events": [Event...], "meta": Meta }
}

Error codes:
- BAD_REQUEST
- NO_LOCATION
- UPSTREAM_ERROR
- INTERNAL_ERROR

## POST /api/chat
Request:
{
  "session_id": "uuid",
  "user_message": "只看周末",
  "current_state": { "location": {"city":"杭州"}, "filters": {...}, "last_events": [{"id":"...","title":"..."}] }
}

Response (ok):
{
  "ok": true,
  "data": {
    "assistant_message": "...",
    "action": { "type": "refetch"|"answer_only", "updated_filters"?: {...}, "focus_event_id"?: "..." },
    "events"?: [Event...],
    "meta"?: Meta
  }
}

Hard rule:
- answer_only must cite evidence_snippets or say insufficient evidence + link.
