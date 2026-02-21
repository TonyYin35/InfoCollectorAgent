from pydantic import BaseModel
from typing import Optional


class Location(BaseModel):
    """Location in search request"""
    city: str
    lat: Optional[float] = None
    lng: Optional[float] = None


class Filters(BaseModel):
    """Filters in search request"""
    time_window_days: int = 7
    categories: list[str] = []
    keyword: str = ""
    limit: int = 10


class SearchRequest(BaseModel):
    """/api/search request per 04_API_SPEC.md"""
    location: Location
    filters: Filters


class LastEvent(BaseModel):
    """Event summary for chat state"""
    id: str
    title: str
