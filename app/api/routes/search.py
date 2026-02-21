"""Search API endpoint"""
import uuid
import logging
from fastapi import APIRouter, HTTPException, Request
from app.schemas.base import ResponseEnvelope, SearchResponse
from app.schemas.search import SearchRequest
from app.pipeline.pipeline import run_pipeline

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/search")
async def search(request: SearchRequest, req: Request) -> ResponseEnvelope[SearchResponse]:
    """
    POST /api/search
    Returns event list based on location and filters
    """
    request_id = str(uuid.uuid4())

    # Extract request details for logging
    location = request.location.model_dump()
    filters = request.filters.model_dump()

    logger.info(
        f"search_request request_id={request_id} location={location} filters={filters}"
    )

    try:
        # Validate location
        if not location.get("city"):
            logger.warning(f"search_request request_id={request_id} error=NO_LOCATION")
            return ResponseEnvelope(
                ok=False,
                error={"code": "NO_LOCATION", "message": "Location city is required"}
            )

        # Run pipeline
        result = await run_pipeline(
            location=location,
            filters=request.filters,
            request_id=request_id
        )

        # Build response
        response_data = SearchResponse(
            events=result.events,
            meta=result.meta.model_dump()
        )

        logger.info(
            f"search_request request_id={request_id} events_count={len(result.events)}"
        )

        return ResponseEnvelope(
            ok=True,
            data=response_data.model_dump()
        )

    except Exception as e:
        logger.error(f"search_request request_id={request_id} error={str(e)}")
        return ResponseEnvelope(
            ok=False,
            error={"code": "INTERNAL_ERROR", "message": str(e)}
        )
