from pydantic import BaseModel
from typing import Optional, Generic, TypeVar


class ErrorDetail(BaseModel):
    """Error detail per 04_API_SPEC.md"""
    code: str  # BAD_REQUEST, NO_LOCATION, UPSTREAM_ERROR, INTERNAL_ERROR
    message: str


T = TypeVar('T')


class ResponseEnvelope(BaseModel, Generic[T]):
    """Unified response envelope per 04_API_SPEC.md"""
    ok: bool
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None


class SearchResponse(BaseModel):
    """/api/search response data"""
    events: list
    meta: dict


class ChatResponse(BaseModel):
    """/api/chat response data"""
    assistant_message: str
    action: dict
    events: Optional[list] = None
    meta: Optional[dict] = None
