"""Provider - returns candidate URLs from fixed sources (Stage 2)"""
from app.pipeline.contract import Plan, CandidateURL


async def get_candidates(plan: Plan) -> list[CandidateURL]:
    """
    Provider: Returns candidate URLs from fixed sources (SOURCES.yaml)
    Input: Plan
    Output: [{url, source_id, source_type, hint_category?}]
    """
    # Stub: Return empty list (no actual providers)
    return []
