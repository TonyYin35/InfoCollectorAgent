"""Chat API endpoint"""
import uuid
import logging
from fastapi import APIRouter, HTTPException, Request
from app.schemas.base import ResponseEnvelope, ChatResponse
from app.schemas.chat import ChatRequest
from chat.graph import run_chat_graph

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/chat")
async def chat(request: ChatRequest, req: Request) -> ResponseEnvelope[ChatResponse]:
    """
    POST /api/chat
    Handles both refetch (update filters) and answer_only (based on evidence)
    """
    request_id = str(uuid.uuid4())

    user_message = request.user_message
    current_state = request.current_state.model_dump()

    logger.info(
        f"chat_request request_id={request_id} session_id={request.session_id} "
        f"message={user_message}"
    )

    try:
        # Run chat graph
        result = await run_chat_graph(
            session_id=request.session_id,
            user_message=user_message,
            current_state=current_state,
            request_id=request_id
        )

        # Build response
        response_data = ChatResponse(
            assistant_message=result.get("assistant_message", ""),
            action=result.get("action", {}),
            events=result.get("events"),
            meta=result.get("meta")
        )

        logger.info(
            f"chat_request request_id={request_id} action={result.get('action', {}).get('type')}"
        )

        return ResponseEnvelope(
            ok=True,
            data=response_data.model_dump()
        )

    except Exception as e:
        logger.error(f"chat_request request_id={request_id} error={str(e)}")
        return ResponseEnvelope(
            ok=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)}
        )
