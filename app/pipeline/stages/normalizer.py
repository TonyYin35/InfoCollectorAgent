"""Normalizer - normalize city/time fields (Stage 5)"""
from app.pipeline.contract import ExtractedEvent, NormalizedEvent


async def normalize_events(extracted: list[ExtractedEvent]) -> list[NormalizedEvent]:
    """
    Normalizer: normalize city/time fields when possible
    """
    # Stub: Return empty list (no actual normalization)
    return []
