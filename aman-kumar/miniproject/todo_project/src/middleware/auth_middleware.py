from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer


# class AuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         if request.url.path.startswith("/tasks"):
#             token = request.headers.get("Authorization")
#             if not token:
#                 return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

# class AuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         if request.url.path.startswith("/tasks"):
#             auth_header = request.headers.get("Authorization")
#             if not auth_header:
#                 return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
#             try:
#                 # Extract token from "Bearer <token>"
#                 scheme, _, token = auth_header.partition(" ")
#                 if scheme.lower() != "bearer" or not token:
#                     return JSONResponse(status_code=401, content={"detail": "Invalid authentication scheme"})
#                 # Validate token by decoding it
#                 username = get_current_user(token)
#                 if not username:
#                     return JSONResponse(status_code=401, content={"detail": "Invalid token"})
#             except HTTPException as e:
#                 return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
#             except JWTError:
#                 return JSONResponse(status_code=401, content={"detail": "Token validation error"})
#         response = await call_next(request)
#         return response



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
                # Optionally, you can set the token in request.state if you want to access it later
                request.state.token = token
                # Do NOT call get_current_user(token) here
            except Exception as e:
                return JSONResponse(status_code=401, content={"detail": "Token validation error"})
        response = await call_next(request)
        return response
