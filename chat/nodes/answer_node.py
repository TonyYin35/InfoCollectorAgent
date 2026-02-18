"""Answer Node - answers based on last_events evidence"""
from typing import TypedDict, Optional


class AnswerResult(TypedDict):
    """Result from AnswerNode"""
    assistant_message: str
    action: dict


async def run_answer(
    user_message: str,
    current_state: dict,
    focus_event_id: Optional[str] = None
) -> AnswerResult:
    """
    AnswerNode:
    - can only use current_state.last_events evidence
    - MUST quote or reference evidence snippets, or say insufficient evidence + primary_source_url

    This is a stub implementation - returns a placeholder response.
    """
    last_events = current_state.get("last_events", [])

    if not last_events:
        return {
            "assistant_message": "抱歉，我没有足够的信息来回答这个问题。请先搜索活动。",
            "action": {
                "type": "answer_only"
            }
        }

    # Stub: Return placeholder message
    return {
        "assistant_message": "这是对您问题的回答。（stub实现）",
        "action": {
            "type": "answer_only"
        }
    }
