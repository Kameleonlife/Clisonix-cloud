import os

import weaviate
from fastapi import APIRouter, Depends, HTTPException

from ..deps import oidc_guard

router = APIRouter(prefix="/bioscience", tags=["bioscience"])


@router.get("/gene/{symbol}")
async def get_gene(symbol: str, user=Depends(oidc_guard)):
    client = weaviate.connect_to_local(
        host=os.getenv("WEAVIATE_URL", "http://weaviate:8080"),
        headers={"X-API-KEY": os.getenv("WEAVIATE_API_KEY", "changeme")},
    )
    try:
        response = client.query.get("Gene", ["symbol", "name", "organism"]).with_where(
            {"path": ["symbol"], "operator": "Equal", "valueText": symbol}
        ).do()
    finally:
        client.close()

    try:
        data = response["data"]["Get"]["Gene"]
    except (KeyError, TypeError):
        data = []

    if not data:
        raise HTTPException(status_code=404, detail="Gene not found")

    return data[0]

