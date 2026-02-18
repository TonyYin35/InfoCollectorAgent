from pydantic import BaseModel
from typing import Optional


class EvidenceSnippet(BaseModel):
    """Evidence snippet from a source"""
    text: str
    url: str


class Event(BaseModel):
    """Event schema per 03_DATA_MODEL.md"""
    id: str
    title: str
    city: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    time_text: Optional[str] = None
    location_text: Optional[str] = None
    signup_hint: Optional[str] = None
    category: str  # "cosplay_convention"|"pop_up"|"meetup_or_photowalk"|"other"
    source_urls: list[str]
    primary_source_url: str
    evidence_snippets: list[EvidenceSnippet]
    fetched_at: str
    published_at: Optional[str] = None
    confidence: str  # "low"|"medium"|"high"


class WarningCode(str):
    """Warning codes per 03_DATA_MODEL.md"""
    LOC_GEO_DENIED = "LOC_GEO_DENIED"
    LOC_GEO_FAILED = "LOC_GEO_FAILED"
    FETCH_TIMEOUT = "FETCH_TIMEOUT"
    FETCH_BLOCKED = "FETCH_BLOCKED"
    EXTRACT_EMPTY = "EXTRACT_EMPTY"
    EXTRACT_LOW_CONF = "EXTRACT_LOW_CONF"
    CANDIDATE_INSUFFICIENT = "CANDIDATE_INSUFFICIENT"
    PROVIDER_DOWN = "PROVIDER_DOWN"


class Warning(BaseModel):
    """Warning per 03_DATA_MODEL.md"""
    code: str
    message: str
    detail: Optional[dict] = None


class SourceUsage(BaseModel):
    """Source usage statistics"""
    source_id: str
    urls_used: int
    success: int
    failed: int


class Meta(BaseModel):
    """Meta information per 03_DATA_MODEL.md"""
    query_plan_summary: str
    sources_used: list[SourceUsage]
    fetched_at: str
    warnings: list[Warning] = []
