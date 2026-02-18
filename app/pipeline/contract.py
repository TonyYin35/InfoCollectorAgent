"""Pipeline stage contracts - defines input/output types for each stage"""
from typing import TypedDict, Optional
from app.schemas.search import Location, Filters


class Plan(TypedDict):
    """Query plan output from BuildPlan"""
    location: Location
    filters: Filters
    sources: list[dict]  # [{source_id, entry_url, ...}]


class CandidateURL(TypedDict):
    """Candidate URL from Provider"""
    url: str
    source_id: str
    source_type: str
    hint_category: Optional[str]


class FetchedPage(TypedDict):
    """Fetched page from Fetcher"""
    url: str
    html: Optional[str]
    status: int
    error: Optional[str]


class ExtractedEvent(TypedDict):
    """Extracted event from Extractor"""
    title: str
    url: str
    evidence_snippets: list[dict]
    raw_fields: dict


class NormalizedEvent(TypedDict):
    """Normalized event from Normalizer"""
    id: str
    title: str
    city: str
    start_time: Optional[str]
    end_time: Optional[str]
    time_text: Optional[str]
    location_text: Optional[str]
    signup_hint: Optional[str]
    category: str
    source_urls: list[str]
    primary_source_url: str
    evidence_snippets: list[dict]
    fetched_at: str
    published_at: Optional[str]
    confidence: str


class ClusteredEvent(TypedDict):
    """Clustered/deduped event"""
    id: str
    title: str
    city: str
    start_time: Optional[str]
    end_time: Optional[str]
    time_text: Optional[str]
    location_text: Optional[str]
    signup_hint: Optional[str]
    category: str
    source_urls: list[str]
    primary_source_url: str
    evidence_snippets: list[dict]
    fetched_at: str
    published_at: Optional[str]
    confidence: str


class RankedEvent(ClusteredEvent):
    """Ranked event with score"""
    score: float
