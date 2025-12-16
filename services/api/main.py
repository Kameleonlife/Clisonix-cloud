from fastapi import FastAPI

from .routers import bioscience, clinical, concept, graph, search, telemetry

app = FastAPI(title="clisonix Knowledge Fabric API")
app.include_router(search.router)
app.include_router(telemetry.router)
app.include_router(clinical.router)
app.include_router(bioscience.router)
app.include_router(concept.router)
app.include_router(graph.router)

