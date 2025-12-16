"""Entry point for the Clisonix FastAPI service."""

from fastapi import FastAPI

from app.Clisonix.routes import router as Clisonix_router

app = FastAPI(title="Clisonix Cloud")

app.include_router(Clisonix_router, prefix="/Clisonix")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=9091)

