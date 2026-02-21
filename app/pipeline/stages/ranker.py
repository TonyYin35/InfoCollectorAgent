"""Ranker - rule-based scoring (Stage 7)"""
from app.pipeline.contract import ClusteredEvent, RankedEvent
from app.schemas.search import Filters


async def rank_events(
    events: list[ClusteredEvent],
    filters: Filters
) -> list[RankedEvent]:
    """
    Rank: rule-based scoring
    Score = time_match + city_match + source_trust + completeness
    """
    # Stub: Return empty list (no actual ranking)
    return []
