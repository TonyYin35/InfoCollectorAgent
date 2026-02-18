"""Fetcher - fetch HTML/text from URLs (Stage 3)"""
from app.pipeline.contract import CandidateURL, FetchedPage


async def fetch_pages(candidates: list[CandidateURL]) -> list[FetchedPage]:
    """
    Fetcher: fetch HTML/text
    Default requests; follow docs/09_FETCH_POLICY.md for Playwright fallback
    """
    # Stub: Return empty list (no actual fetching)
    return []
