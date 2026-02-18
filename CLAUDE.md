# InfoCollectorAgent (Info Radar)

AI-powered event discovery platform for local activities (漫展/快闪/同好活动) in China Mainland cities.

## Project Overview

**Info Radar (信息雷达)** is a retrieval + aggregation + summarization assistant for discovering local events. Users view a webpage, the system auto-retrieves event information based on location/city and default filters, outputs structured event cards, and allows users to modify filters or追问 details via chat.

### Core Principles
- **Traceable**: Every result has source evidence
- **Deduplicable**: Same event from multiple sources merged
- **Filterable**: By time/distance/category

## Tech Stack

- **LangGraph** - Multi-agent workflow orchestration
- **Google Gemini** - LLM for chat and reasoning
- **Python** - Backend API and pipeline
- **FastAPI** - Web framework
- **pytest** - Unit testing

## Documentation Structure

All requirements are in `docs/` - this is the Single Source of Truth:

| File | Purpose |
|------|---------|
| `01_PRD_MVP.md` | Product requirements & acceptance criteria |
| `02_ARCHITECTURE.md` | Engineering modules, directory structure |
| `03_DATA_MODEL.md` | Event, Meta, Warning, QuerySpec schemas |
| `04_API_SPEC.md` | /api/search and /api/chat specs |
| `05_PIPELINE_SPEC.md` | Retrieval pipeline stages |
| `06_CHAT_LANGGRAPH.md` | LangGraph graph, nodes, tools |
| `07_SOURCES.yaml` | Fixed site entry list |
| `08_CATEGORY_MAP.json` | Category enum & keyword mapping |
| `09_FETCH_POLICY.md` | requests vs Playwright strategy |
| `10_PROMPTS.md` | LLM prompts (routing/extraction fallback) |
| `11_TEST_PLAN.md` | Executable acceptance test cases |
| `12_RUNBOOK.md` | Local setup, env vars, troubleshooting |
| `13_BACKLOG.md` | Post-MVP iteration list |
| `14_ADR.md` | Architecture decision records |

## Implemented Components

### Project Structure
```
InfoCollectorAgent/
├── CLAUDE.md                    # This file
├── requirements.txt             # Python dependencies
├── app/                         # Main application
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # Configuration management
│   ├── logging_config.py        # JSON structured logging
│   ├── schemas/                 # Pydantic models
│   │   ├── base.py              # ResponseEnvelope
│   │   ├── event.py             # Event, Meta, Warning, SourceUsage
│   │   ├── search.py            # SearchRequest, Location, Filters
│   │   └── chat.py              # ChatRequest, CurrentState
│   ├── api/
│   │   ├── deps.py              # Dependency injection
│   │   └── routes/
│   │       ├── search.py        # /api/search endpoint
│   │       └── chat.py          # /api/chat endpoint
│   └── pipeline/
│       ├── contract.py           # Pipeline stage contracts (TypedDict)
│       ├── pipeline.py           # Pipeline orchestrator with timing
│       └── stages/               # Pipeline stage stubs
│           ├── query_builder.py  # Stage 1: BuildPlan
│           ├── provider.py       # Stage 2: Provider
│           ├── fetcher.py       # Stage 3: Fetcher
│           ├── extractor.py      # Stage 4: Extractor
│           ├── normalizer.py     # Stage 5: Normalizer
│           ├── deduplicator.py   # Stage 6: Cluster/Dedupe
│           ├── ranker.py        # Stage 7: Rank
│           └── evidence_checker.py # Stage 8: EvidenceCheck
├── cache/
│   ├── base.py                  # CacheBackend interface (Protocol)
│   └── memory.py                # MemoryCache implementation
├── chat/
│   ├── graph.py                 # LangGraph chat orchestrator
│   └── nodes/
│       ├── parse_intent.py       # ParseIntentNode
│       ├── search_node.py       # SearchNode
│       └── answer_node.py       # AnswerNode
├── demo_agent/                   # Existing demo (preserved)
└── docs/                        # Requirements (Single Source of Truth)
```

### Features Implemented
- ✅ FastAPI server running on port 8000
- ✅ `/api/search` endpoint - returns events based on location/filters
- ✅ `/api/chat` endpoint - handles refetch and answer_only intents
- ✅ Unified response envelope (`ok`, `data`, `error`)
- ✅ Error codes (BAD_REQUEST, NO_LOCATION, UPSTREAM_ERROR, INTERNAL_ERROR)
- ✅ JSON structured logging with request_id and stage timing
- ✅ Pipeline orchestration with 8 stages (stubs returning empty lists)
- ✅ Replacable cache interface (default: MemoryCache)
- ✅ LangGraph chat router (refetch vs answer_only)

### Not Implemented (MVP Skeleton)
- ❌ Real web scraping/fetching
- ❌ Event extraction from HTML
- ❌ Deduplication logic
- ❌ Ranking algorithm
- ❌ Provider adapters (SOURCES.yaml)

## API Endpoints

### POST /api/search
```json
Request:
{
  "location": { "city": "杭州" },
  "filters": { "time_window_days": 7, "categories": ["cosplay_convention","pop_up"], "keyword": "", "limit": 10 }
}

Response:
{
  "ok": true,
  "data": { "events": [Event...], "meta": Meta }
}
```

### POST /api/chat
```json
Request:
{
  "session_id": "uuid",
  "user_message": "只看周末",
  "current_state": { "location": {"city":"杭州"}, "filters": {...}, "last_events": [...] }
}

Response:
{
  "ok": true,
  "data": {
    "assistant_message": "...",
    "action": { "type": "refetch"|"answer_only", "updated_filters"?: {...}, "focus_event_id"?: "..." },
    "events"?: [Event...],
    "meta"?: Meta
  }
}
```

## Key Constraints

1. **China Mainland cities only** - City-level "nearby" via string match
2. **Fixed site entry recall** - No general search engine in MVP
3. **On-demand crawling** - Refresh triggers pipeline
4. **Evidence citation required** - answer_only must cite evidence_snippets or say insufficient evidence + link

## Categories (MVP)

- `cosplay_convention` - 漫展
- `pop_up` - 快闪
- `meetup_or_photowalk` - 同好活动/外拍
- `other`

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_schemas.py -v

# Run with coverage
pytest tests/ --cov=app --cov=chat --cov=cache
```

## Environment Variables

- `GOOGLE_API_KEY` - Required for Gemini LLM
- `API_HOST` - Server host (default: 0.0.0.0)
- `API_PORT` - Server port (default: 8000)
- `LOG_LEVEL` - Logging level (default: INFO)
- `CACHE_TTL` - Cache TTL in seconds (default: 300)
- `PIPELINE_TIMEOUT` - Pipeline timeout in seconds (default: 30)
