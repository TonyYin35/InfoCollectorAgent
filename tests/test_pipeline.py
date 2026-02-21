"""Tests for pipeline"""
import pytest
from app.pipeline.pipeline import run_pipeline, get_filter_limit, get_filter_value
from app.schemas.search import Location, Filters


class TestPipelineHelperFunctions:
    """Test pipeline helper functions"""

    def test_get_filter_limit_with_filters(self):
        """Test get_filter_limit with Filters object"""
        filters = Filters(limit=20)
        result = get_filter_limit(filters)
        assert result == 20

    def test_get_filter_limit_with_dict(self):
        """Test get_filter_limit with dict"""
        filters = {"limit": 15}
        result = get_filter_limit(filters)
        assert result == 15

    def test_get_filter_limit_default(self):
        """Test get_filter_limit default value"""
        filters = {}
        result = get_filter_limit(filters)
        assert result == 10  # default

    def test_get_filter_value_with_filters(self):
        """Test get_filter_value with Filters object"""
        filters = Filters(time_window_days=14)
        result = get_filter_value(filters, "time_window_days")
        assert result == 14

    def test_get_filter_value_with_dict(self):
        """Test get_filter_value with dict"""
        filters = {"time_window_days": 30}
        result = get_filter_value(filters, "time_window_days")
        assert result == 30

    def test_get_filter_value_default(self):
        """Test get_filter_value default value"""
        filters = {}
        result = get_filter_value(filters, "time_window_days", 7)
        assert result == 7


class TestPipeline:
    """Test pipeline execution"""

    @pytest.mark.asyncio
    async def test_pipeline_returns_empty_events(self):
        """Test pipeline returns empty events list (stub)"""
        location = Location(city="杭州")
        filters = Filters(time_window_days=7, categories=[], keyword="", limit=10)

        result = await run_pipeline(location=location, filters=filters)

        assert result.events == []
        assert result.meta is not None

    @pytest.mark.asyncio
    async def test_pipeline_returns_meta(self):
        """Test pipeline returns meta information"""
        location = Location(city="杭州")
        filters = Filters(time_window_days=7, categories=[], keyword="", limit=10)

        result = await run_pipeline(location=location, filters=filters)

        assert result.meta.query_plan_summary is not None
        assert "杭州" in result.meta.query_plan_summary
        assert result.meta.fetched_at is not None

    @pytest.mark.asyncio
    async def test_pipeline_with_different_city(self):
        """Test pipeline with different city"""
        location = Location(city="北京")
        filters = Filters(time_window_days=30, categories=["pop_up"], keyword="", limit=5)

        result = await run_pipeline(location=location, filters=filters)

        assert "北京" in result.meta.query_plan_summary
        assert result.events == []

    @pytest.mark.asyncio
    async def test_pipeline_with_request_id(self):
        """Test pipeline accepts request_id"""
        location = Location(city="上海")
        filters = Filters()

        result = await run_pipeline(
            location=location,
            filters=filters,
            request_id="custom-request-id"
        )

        assert result.meta is not None
