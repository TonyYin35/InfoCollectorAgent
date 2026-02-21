"""Test configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def search_request_payload():
    """Sample search request payload"""
    return {
        "location": {"city": "杭州"},
        "filters": {
            "time_window_days": 7,
            "categories": ["cosplay_convention", "pop_up"],
            "keyword": "",
            "limit": 10
        }
    }


@pytest.fixture
def chat_request_payload():
    """Sample chat request payload"""
    return {
        "session_id": "test-session-123",
        "user_message": "只看周末",
        "current_state": {
            "location": {"city": "杭州"},
            "filters": {
                "time_window_days": 7,
                "categories": ["cosplay_convention"],
                "keyword": "",
                "limit": 10
            },
            "last_events": []
        }
    }
