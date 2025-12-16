import os

import weaviate
from fastapi import APIRouter, Depends, Query

from ..deps import oidc_guard

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
async def search(q: str = Query(..., min_length=2), user=Depends(oidc_guard)):
    host = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
    api_key = os.getenv("WEAVIATE_API_KEY", "changeme")
    client = weaviate.connect_to_local(host=host, headers={"X-API-KEY": api_key})
    try:
        response = client.query.near_text("Paper", query=q, limit=10)
        return {"results": response}
    finally:
        client.close()

