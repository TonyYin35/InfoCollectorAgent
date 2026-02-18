"""Parse Intent Node - determines if user wants refetch or answer_only"""
from typing import TypedDict, Optional


class Intent(TypedDict):
    """Parsed intent from user message"""
    type: str  # "refetch" | "answer_only"
    updated_filters: Optional[dict]
    focus_event_id: Optional[str]


# Refetch trigger keywords (MVP)
REFETCH_TIME_TERMS = {"今天", "本周", "周末", "未来7天", "未来30天"}
REFETCH_LOCATION_TERMS = {"市", "区", "县"}  # Simple city/area detection
REFETCH_CATEGORY_TERMS = {"漫展", "快闪", "外拍", "同好会"}
REFETCH_LIMIT_TERMS = {"5", "10", "20"}

# Answer_only trigger keywords (MVP)
ANSWER_ONLY_TERMS = {"报名", "买票", "几点", "地点", "费用", "交通", "官网", "主办", "怎么", "如何"}


def parse_intent(user_message: str, current_state: dict) -> Intent:
    """
    ParseIntentNode:
    - input: user_message, current_state
    - output: intent {type, updated_filters?, focus_event_id?}
    """
    msg = user_message.lower()

    # Check for answer_only first (detail questions)
    for term in ANSWER_ONLY_TERMS:
        if term in msg:
            return {
                "type": "answer_only",
                "updated_filters": None,
                "focus_event_id": None
            }

    # Check for refetch triggers (filter changes)
    updated_filters = {}
    filters = current_state.get("filters", {})

    # Time filter
    if "今天" in msg:
        updated_filters["time_window_days"] = 1
    elif "本周" in msg or "周末" in msg:
        updated_filters["time_window_days"] = 7
    elif "未来7天" in msg:
        updated_filters["time_window_days"] = 7
    elif "未来30天" in msg:
        updated_filters["time_window_days"] = 30

    # Category filter
    if "漫展" in msg:
        updated_filters.setdefault("categories", []).append("cosplay_convention")
    elif "快闪" in msg:
        updated_filters.setdefault("categories", []).append("pop_up")
    elif "外拍" in msg or "同好会" in msg:
        updated_filters.setdefault("categories", []).append("meetup_or_photowalk")

    # Limit filter
    if "5条" in msg or "5 条" in msg:
        updated_filters["limit"] = 5
    elif "10条" in msg or "10 条" in msg:
        updated_filters["limit"] = 10
    elif "20条" in msg or "20 条" in msg:
        updated_filters["limit"] = 20

    # If any filters updated, it's a refetch
    if updated_filters:
        return {
            "type": "refetch",
            "updated_filters": {**filters, **updated_filters},
            "focus_event_id": None
        }

    # Default to answer_only
    return {
        "type": "answer_only",
        "updated_filters": None,
        "focus_event_id": None
    }
