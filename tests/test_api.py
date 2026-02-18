"""Tests for API endpoints"""
import pytest


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check(self, client):
        """Test /health endpoint returns ok"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "InfoCollectorAgent"
        assert "version" in data


class TestSearchEndpoint:
    """Test /api/search endpoint"""

    def test_search_success(self, client, search_request_payload):
        """Test successful search request"""
        response = client.post("/api/search", json=search_request_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert "data" in data
        assert "events" in data["data"]
        assert "meta" in data["data"]

    def test_search_with_different_city(self, client):
        """Test search with different city"""
        payload = {
            "location": {"city": "北京"},
            "filters": {"time_window_days": 7, "categories": [], "keyword": "", "limit": 10}
        }
        response = client.post("/api/search", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert "北京" in data["data"]["meta"]["query_plan_summary"]

    def test_search_with_categories(self, client):
        """Test search with categories"""
        payload = {
            "location": {"city": "杭州"},
            "filters": {
                "time_window_days": 7,
                "categories": ["cosplay_convention", "pop_up"],
                "keyword": "",
                "limit": 10
            }
        }
        response = client.post("/api/search", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert "cosplay_convention" in data["data"]["meta"]["query_plan_summary"]

    def test_search_missing_city(self, client):
        """Test search with missing city - Pydantic validation fails"""
        payload = {
            "location": {},  # Missing required 'city' field
            "filters": {"time_window_days": 7, "categories": [], "keyword": "", "limit": 10}
        }
        response = client.post("/api/search", json=payload)
        # Pydantic returns 422 validation error for missing required field
        assert response.status_code == 422


class TestChatEndpoint:
    """Test /api/chat endpoint"""

    def test_chat_refetch(self, client, chat_request_payload):
        """Test chat with refetch intent"""
        response = client.post("/api/chat", json=chat_request_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert data["data"]["action"]["type"] == "refetch"
        assert "assistant_message" in data["data"]

    def test_chat_answer_only(self, client):
        """Test chat with answer_only intent"""
        payload = {
            "session_id": "test-session",
            "user_message": "这个活动怎么报名？",
            "current_state": {
                "location": {"city": "杭州"},
                "filters": {"time_window_days": 7, "categories": [], "keyword": "", "limit": 10},
                "last_events": [{"id": "1", "title": "test event"}]
            }
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert data["data"]["action"]["type"] == "answer_only"

    def test_chat_weekend_refetch(self, client):
        """Test chat with weekend refetch"""
        payload = {
            "session_id": "test-session",
            "user_message": "只看周末",
            "current_state": {
                "location": {"city": "杭州"},
                "filters": {"time_window_days": 7, "categories": [], "keyword": "", "limit": 10},
                "last_events": []
            }
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert data["data"]["action"]["type"] == "refetch"
