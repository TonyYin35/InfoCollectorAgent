"""Pipeline orchestrator - runs all stages in sequence with timing"""
import time
import uuid
from typing import Any, Optional, Dict, List, Union
from datetime import datetime
from dataclasses import dataclass

from app.schemas.search import Location, Filters
from app.schemas.event import Meta, Warning, SourceUsage
from app.pipeline.contract import (
    Plan, CandidateURL, FetchedPage, ExtractedEvent,
    NormalizedEvent, ClusteredEvent, RankedEvent
)
from app.pipeline.stages import (
    query_builder,
    provider,
    fetcher,
    extractor,
    normalizer,
    deduplicator,
    ranker,
    evidence_checker
)


@dataclass
class PipelineResult:
    """Pipeline execution result"""
    events: List[dict]
    meta: Meta


def get_filter_limit(filters: Union[Filters, dict]) -> int:
    """Get limit from filters - handles both Pydantic model and dict"""
    if isinstance(filters, Filters):
        return filters.limit
    return filters.get("limit", 10)


def get_filter_value(filters: Union[Filters, dict], key: str, default: Any = None) -> Any:
    """Get value from filters - handles both Pydantic model and dict"""
    if isinstance(filters, Filters):
        return getattr(filters, key, default)
    return filters.get(key, default)


async def run_pipeline(
    location: Union[Location, dict],
    filters: Union[Filters, dict],
    request_id: Optional[str] = None
) -> PipelineResult:
    """
    Run full retrieval pipeline with timing tracking
    Stages:
    1) BuildPlan -> Plan
    2) Provider -> candidate_urls[]
    3) Fetch -> pages[]
    4) Extract -> extracted_events[]
    5) Normalize -> normalized_events[]
    6) Cluster/Dedupe -> clustered_events[]
    7) Rank -> ranked_events[]
    8) EvidenceCheck -> final_events[]
    9) Return(events, meta)
    """
    if request_id is None:
        request_id = str(uuid.uuid4())

    stage_timing: Dict[str, float] = {}
    warnings: List[Warning] = []
    sources_used: List[SourceUsage] = []

    # Get city for logging
    city = get_filter_value(location, "city", "unknown") if isinstance(location, dict) else location.city

    # Stage 1: BuildPlan
    start = time.perf_counter()
    plan: Plan = await query_builder.build_plan(location, filters)
    stage_timing["build_plan"] = time.perf_counter() - start

    # Stage 2: Provider
    start = time.perf_counter()
    candidates: List[CandidateURL] = await provider.get_candidates(plan)
    stage_timing["provider"] = time.perf_counter() - start

    # Stage 3: Fetcher
    start = time.perf_counter()
    pages: List[FetchedPage] = await fetcher.fetch_pages(candidates)
    stage_timing["fetcher"] = time.perf_counter() - start

    # Stage 4: Extractor
    start = time.perf_counter()
    extracted: List[ExtractedEvent] = await extractor.extract_events(pages)
    stage_timing["extractor"] = time.perf_counter() - start

    # Stage 5: Normalizer
    start = time.perf_counter()
    normalized: List[NormalizedEvent] = await normalizer.normalize_events(extracted)
    stage_timing["normalizer"] = time.perf_counter() - start

    # Stage 6: Deduplicator
    start = time.perf_counter()
    clustered: List[ClusteredEvent] = await deduplicator.deduplicate_events(
        normalized, filters
    )
    stage_timing["deduplicator"] = time.perf_counter() - start

    # Stage 7: Ranker
    start = time.perf_counter()
    ranked: List[RankedEvent] = await ranker.rank_events(clustered, filters)
    stage_timing["ranker"] = time.perf_counter() - start

    # Stage 8: Evidence Check
    start = time.perf_counter()
    final_events: List[ClusteredEvent] = await evidence_checker.check_evidence(ranked)
    stage_timing["evidence_check"] = time.perf_counter() - start

    # Apply limit
    limit = get_filter_limit(filters)
    final_events = final_events[:limit]

    # Build meta
    fetched_at = datetime.utcnow().isoformat() + "Z"
    time_window = get_filter_value(filters, "time_window_days", 7)
    categories = get_filter_value(filters, "categories", [])
    query_plan_summary = f"location={city}, time_window={time_window}d, categories={categories}, limit={limit}"

    meta = Meta(
        query_plan_summary=query_plan_summary,
        sources_used=sources_used,
        fetched_at=fetched_at,
        warnings=warnings
    )

    return PipelineResult(
        events=[dict(e) for e in final_events],
        meta=meta
    )
