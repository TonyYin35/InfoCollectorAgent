"""Extractor - parse Event fields + evidence snippets (Stage 4)"""
from app.pipeline.contract import FetchedPage, ExtractedEvent


async def extract_events(pages: list[FetchedPage]) -> list[ExtractedEvent]:
    """
    Extractor: parse Event fields + evidence snippets
    Output must include:
    - title (or fallback from page title)
    - evidence_snippets (>=1 if any content exists)
    """
    # Stub: Return empty list (no actual extraction)
    return []
