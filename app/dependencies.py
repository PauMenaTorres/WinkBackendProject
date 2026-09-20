import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

security = HTTPBearer()

def verify_admin_token(authentication: HTTPAuthorizationCredentials = Security(security)) -> str:
    if authentication.credentials != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authentication.credentials
