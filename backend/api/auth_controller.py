from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4
import hashlib

router = APIRouter()
API_KEYS = {}

class RegisterRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register_user(payload: RegisterRequest):
    if payload.email in API_KEYS:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = hashlib.sha256(payload.password.encode()).hexdigest()
    api_key = f"NSX_{uuid4().hex}"
    API_KEYS[payload.email] = {"password": hashed, "api_key": api_key}
    return {"email": payload.email, "api_key": api_key}

@router.post("/login")
def login_user(payload: RegisterRequest):
    user = API_KEYS.get(payload.email)
    if not user or user["password"] != hashlib.sha256(payload.password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"api_key": user["api_key"]}

