from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok", "service": "Clisonix Health", "port": 8088}


