"""LangGraph Chat Router - decides refetch vs answer_only"""
from typing import TypedDict
from chat.nodes.parse_intent import parse_intent, Intent
from chat.nodes.search_node import run_search
from chat.nodes.answer_node import run_answer


class GraphState(TypedDict):
    """State passed through the graph"""
    user_message: str
    current_state: dict
    intent: Intent
    result: dict


async def run_chat_graph(
    session_id: str,
    user_message: str,
    current_state: dict,
    request_id: str
) -> dict:
    """
    Run chat graph:
    1) ParseIntentNode -> determine refetch or answer_only
    2) If refetch -> SearchNode -> runs pipeline with updated filters
    3) If answer_only -> AnswerNode -> answer based on evidence

    Returns:
    {
        "assistant_message": str,
        "action": {"type": "refetch"|"answer_only", ...},
        "events": list | None,
        "meta": dict | None
    }
    """
    # Step 1: Parse intent
    intent = parse_intent(user_message, current_state)

    if intent["type"] == "refetch":
        # Refetch: run search with updated filters
        updated_filters = intent.get("updated_filters", {})
        location = current_state.get("location", {})

        search_result = await run_search(
            location=location,
            filters=updated_filters,
            request_id=request_id
        )

        return {
            "assistant_message": "已根据您的要求更新筛选条件，这是最新的活动列表。",
            "action": {
                "type": "refetch",
                "updated_filters": updated_filters
            },
            "events": search_result.get("events"),
            "meta": search_result.get("meta")
        }

    else:
        # Answer only: respond based on evidence
        answer_result = await run_answer(
            user_message=user_message,
            current_state=current_state,
            focus_event_id=intent.get("focus_event_id")
        )

        return {
            "assistant_message": answer_result["assistant_message"],
            "action": answer_result["action"],
            "events": None,
            "meta": None
        }
