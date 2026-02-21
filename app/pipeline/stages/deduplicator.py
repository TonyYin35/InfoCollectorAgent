"""Deduplicator - merge duplicates (Stage 6)"""
from app.pipeline.contract import NormalizedEvent, ClusteredEvent
from app.schemas.search import Filters


async def deduplicate_events(
    events: list[NormalizedEvent],
    filters: Filters
) -> list[ClusteredEvent]:
    """
    Cluster/Dedupe: merge duplicates
    Rule (MVP):
    - same URL => same item
    - high title similarity + near time clue + near location clue => merge
    - merged keeps multiple source_urls; choose primary by (source trust + completeness)
    """
    # Stub: Return empty list (no actual deduplication)
    return []
