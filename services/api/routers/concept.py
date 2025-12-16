from fastapi import APIRouter, Body, Depends

from ..deps import oidc_guard

router = APIRouter(prefix="/concept-suggestions", tags=["concepts"])


@router.post("")
async def suggest_concepts(payload: dict = Body(...), user=Depends(oidc_guard)):
    residual = float(payload.get("residual", 0.0))
    gap_detected = residual > 0.6
    return {
        "gap": gap_detected,
        "residual": residual,
        "action": "summarize_and_seed" if gap_detected else "no_action",
    }

