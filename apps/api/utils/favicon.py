from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

def add_favicon_route(app: FastAPI):
    favicon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
    if not os.path.exists(favicon_path):
        # Create a simple blank favicon if missing
        with open(favicon_path, "wb") as f:
            f.write(bytes([0] * 318))  # 16x16 blank ico
    @app.get("/favicon.ico", include_in_schema=False)
    def favicon():
        return FileResponse(favicon_path, media_type="image/x-icon")


