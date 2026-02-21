"""Query Builder - builds query plan from location + filters (Stage 1)"""
from app.pipeline.contract import Plan
from app.schemas.search import Location, Filters


async def build_plan(location: Location, filters: Filters) -> Plan:
    """
    BuildPlan: Build query plan from location + filters
    Returns Plan with sources to query
    """
    # Stub: Return empty sources list (no actual providers)
    return {
        "location": location,
        "filters": filters,
        "sources": []
    }
