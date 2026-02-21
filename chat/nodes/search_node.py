"""Search Node - runs pipeline with updated filters"""
from app.pipeline.pipeline import run_pipeline


async def run_search(
    location: dict,
    filters: dict,
    request_id: str
) -> dict:
    """
    SearchNode:
    - runs pipeline with updated filters
    - returns events + meta
    """
    result = await run_pipeline(
        location=location,
        filters=filters,
        request_id=request_id
    )

    return {
        "events": result.events,
        "meta": result.meta.model_dump()
    }
