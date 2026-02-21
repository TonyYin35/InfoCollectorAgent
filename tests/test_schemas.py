"""Tests for Pydantic schemas"""
import pytest
from app.schemas.event import Event, EvidenceSnippet, Meta, Warning, SourceUsage
from app.schemas.search import SearchRequest, Location, Filters
from app.schemas.chat import ChatRequest, CurrentState
from app.schemas.base import ResponseEnvelope, SearchResponse, ChatResponse


class TestEventSchema:
    """Test Event schema"""

    def test_event_with_all_fields(self):
        """Test Event with all fields"""
        event = Event(
            id="test-1",
            title="测试活动",
            city="杭州",
            start_time="2024-01-01T10:00:00Z",
            end_time="2024-01-01T18:00:00Z",
            time_text="2024年1月1日",
            location_text="杭州国际会展中心",
            signup_hint="需要报名",
            category="cosplay_convention",
            source_urls=["https://example.com/1"],
            primary_source_url="https://example.com/1",
            evidence_snippets=[
                EvidenceSnippet(text="活动详情", url="https://example.com/1")
            ],
            fetched_at="2024-01-01T00:00:00Z",
            published_at="2023-12-01T00:00:00Z",
            confidence="high"
        )
        assert event.id == "test-1"
        assert event.title == "测试活动"
        assert event.category == "cosplay_convention"
        assert event.confidence == "high"

    def test_event_minimal_fields(self):
        """Test Event with minimal fields"""
        event = Event(
            id="test-2",
            title="测试活动",
            city="杭州",
            category="other",
            source_urls=["https://example.com/2"],
            primary_source_url="https://example.com/2",
            evidence_snippets=[],
            fetched_at="2024-01-01T00:00:00Z",
            confidence="low"
        )
        assert event.id == "test-2"
        assert event.start_time is None
        assert event.signup_hint is None


class TestSearchRequestSchema:
    """Test SearchRequest schema"""

    def test_valid_search_request(self):
        """Test valid search request"""
        req = SearchRequest(
            location=Location(city="杭州"),
            filters=Filters(
                time_window_days=7,
                categories=["cosplay_convention"],
                keyword="漫展",
                limit=10
            )
        )
        assert req.location.city == "杭州"
        assert req.filters.time_window_days == 7
        assert req.filters.limit == 10

    def test_search_request_defaults(self):
        """Test search request with defaults"""
        req = SearchRequest(
            location=Location(city="北京"),
            filters=Filters()
        )
        assert req.filters.time_window_days == 7  # default
        assert req.filters.limit == 10  # default
        assert req.filters.categories == []  # default


class TestChatRequestSchema:
    """Test ChatRequest schema"""

    def test_valid_chat_request(self):
        """Test valid chat request"""
        req = ChatRequest(
            session_id="session-123",
            user_message="只看周末",
            current_state=CurrentState(
                location=Location(city="杭州"),
                filters=Filters(time_window_days=7, categories=[], keyword="", limit=10),
                last_events=[]
            )
        )
        assert req.session_id == "session-123"
        assert req.user_message == "只看周末"


class TestResponseEnvelope:
    """Test ResponseEnvelope"""

    def test_success_response(self):
        """Test success response envelope"""
        response = ResponseEnvelope(
            ok=True,
            data={"events": [], "meta": {}}
        )
        assert response.ok is True
        assert response.data is not None
        assert response.error is None

    def test_error_response(self):
        """Test error response envelope"""
        response = ResponseEnvelope(
            ok=False,
            error={"code": "BAD_REQUEST", "message": "Invalid request"}
        )
        assert response.ok is False
        assert response.error is not None
        assert response.error.code == "BAD_REQUEST"


class TestMetaSchema:
    """Test Meta schema"""

    def test_meta_with_all_fields(self):
        """Test Meta with all fields"""
        meta = Meta(
            query_plan_summary="location=杭州, time_window=7d",
            sources_used=[
                SourceUsage(source_id="source1", urls_used=5, success=4, failed=1)
            ],
            fetched_at="2024-01-01T00:00:00Z",
            warnings=[
                Warning(code="FETCH_TIMEOUT", message="Request timed out")
            ]
        )
        assert meta.query_plan_summary == "location=杭州, time_window=7d"
        assert len(meta.sources_used) == 1
        assert len(meta.warnings) == 1

    def test_meta_empty_fields(self):
        """Test Meta with empty optional fields"""
        meta = Meta(
            query_plan_summary="test",
            sources_used=[],
            fetched_at="2024-01-01T00:00:00Z"
        )
        assert meta.warnings == []
