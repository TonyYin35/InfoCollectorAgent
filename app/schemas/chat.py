from pydantic import BaseModel
from typing import Optional
from .search import Location, Filters, LastEvent


class CurrentState(BaseModel):
    """Current state in chat request"""
    location: Location
    filters: Filters
    last_events: list[LastEvent]


class ChatRequest(BaseModel):
    """/api/chat request per 04_API_SPEC.md"""
    session_id: str
    user_message: str
    current_state: CurrentState
