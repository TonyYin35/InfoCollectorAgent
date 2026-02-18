"""Tests for chat nodes"""
import pytest
from chat.nodes.parse_intent import parse_intent


class TestParseIntent:
    """Test parse_intent function"""

    def test_refetch_time_today(self):
        """Test refetch with '今天'"""
        intent = parse_intent("只看今天", {})
        assert intent["type"] == "refetch"
        assert intent["updated_filters"]["time_window_days"] == 1

    def test_refetch_time_weekend(self):
        """Test refetch with '周末'"""
        intent = parse_intent("只看周末", {})
        assert intent["type"] == "refetch"
        assert intent["updated_filters"]["time_window_days"] == 7

    def test_refetch_time_week(self):
        """Test refetch with '本周'"""
        intent = parse_intent("本周活动", {})
        assert intent["type"] == "refetch"
        assert intent["updated_filters"]["time_window_days"] == 7

    def test_refetch_time_30_days(self):
        """Test refetch with '未来30天'"""
        intent = parse_intent("未来30天", {})
        assert intent["type"] == "refetch"
        assert intent["updated_filters"]["time_window_days"] == 30

    def test_refetch_category_cosplay(self):
        """Test refetch with '漫展'"""
        intent = parse_intent("漫展活动", {})
        assert intent["type"] == "refetch"
        assert "cosplay_convention" in intent["updated_filters"]["categories"]

    def test_refetch_category_popup(self):
        """Test refetch with '快闪'"""
        intent = parse_intent("快闪活动", {})
        assert intent["type"] == "refetch"
        assert "pop_up" in intent["updated_filters"]["categories"]

    def test_refetch_limit_5(self):
        """Test refetch with limit 5"""
        intent = parse_intent("给我5条", {})
        assert intent["type"] == "refetch"
        assert intent["updated_filters"]["limit"] == 5

    def test_refetch_limit_20(self):
        """Test refetch with limit 20"""
        intent = parse_intent("20条活动", {})
        assert intent["type"] == "refetch"
        assert intent["updated_filters"]["limit"] == 20

    def test_answer_only_registration(self):
        """Test answer_only with '报名'"""
        intent = parse_intent("怎么报名？", {})
        assert intent["type"] == "answer_only"

    def test_answer_only_ticket(self):
        """Test answer_only with '买票'"""
        intent = parse_intent("在哪里买票？", {})
        assert intent["type"] == "answer_only"

    def test_answer_only_location(self):
        """Test answer_only with '地点'"""
        intent = parse_intent("活动地点在哪里？", {})
        assert intent["type"] == "answer_only"

    def test_answer_only_price(self):
        """Test answer_only with '费用'"""
        intent = parse_intent("需要费用吗？", {})
        assert intent["type"] == "answer_only"

    def test_default_answer_only(self):
        """Test default to answer_only"""
        intent = parse_intent("你好", {})
        assert intent["type"] == "answer_only"

    def test_refetch_preserves_existing_filters(self):
        """Test refetch preserves existing filters"""
        current_state = {
            "filters": {
                "time_window_days": 30,
                "categories": ["cosplay_convention"],
                "limit": 20
            }
        }
        intent = parse_intent("只看周末", current_state)
        assert intent["type"] == "refetch"
        assert intent["updated_filters"]["time_window_days"] == 7
        assert intent["updated_filters"]["categories"] == ["cosplay_convention"]
        assert intent["updated_filters"]["limit"] == 20
