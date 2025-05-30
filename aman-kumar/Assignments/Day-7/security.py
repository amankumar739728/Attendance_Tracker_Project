from passlib.context import CryptContext
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/tasks"):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
            try:
                # Extract token from "Bearer <token>"
                scheme, _, token = auth_header.partition(" ")
                # Check if the scheme is "Bearer" and token is not empty
                if scheme.lower() != "bearer" or not token:
                    return JSONResponse(status_code=401, content={"detail": "Invalid authentication scheme"})
                request.state.token = token
            except Exception as e:
                return JSONResponse(status_code=401, content={"detail": "Token validation error"})
        response = await call_next(request)
        return response
    
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
        
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)