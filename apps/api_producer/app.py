from fastapi import FastAPI

app = FastAPI(title="api_producer")


@app.get("/status")
def status():
    return {"app": "api_producer", "status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.api_producer.app:app", host="0.0.0.0", port=8102, log_level="info")

