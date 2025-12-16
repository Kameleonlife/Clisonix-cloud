import os
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from neo4j import GraphDatabase

from ..deps import oidc_guard

router = APIRouter(prefix="/graph", tags=["graph"])

_driver = GraphDatabase.driver(
    os.getenv("NEO4J_URL", "bolt://neo4j:7687"),
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "test1234")),
)


@router.get("/concept/{term}")
async def concept(term: str, user=Depends(oidc_guard)) -> List[Dict[str, Any]]:
    with _driver.session() as session:
        results = session.run(
            """
            MATCH (c:Concept)
            WHERE toLower(c.name) CONTAINS toLower($term)
            OPTIONAL MATCH (c)-[r]->(d)
            RETURN c, collect({rel: type(r), to: d}) AS rels
            LIMIT 50
            """,
            term=term,
        )
        payload: List[Dict[str, Any]] = []
        for record in results:
            concept_node = record[0]
            relationships = record[1]
            payload.append(
                {
                    "id": concept_node.get("id"),
                    "name": concept_node.get("name"),
                    "relationships": [
                        {
                            "type": rel.get("rel"),
                            "to": rel.get("to").get("name") if rel.get("to") else None,
                        }
                        for rel in relationships
                        if rel
                    ],
                }
            )
        return payload

