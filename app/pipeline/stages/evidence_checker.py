"""Evidence Checker - ensure each Event has >=1 evidence snippet (Stage 8)"""
from app.pipeline.contract import RankedEvent, ClusteredEvent


async def check_evidence(events: list[RankedEvent]) -> list[ClusteredEvent]:
    """
    EvidenceCheck: ensure each Event has >=1 evidence snippet
    """
    # Stub: Return empty list (no actual checking)
    return []
