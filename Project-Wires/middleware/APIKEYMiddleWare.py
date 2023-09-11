from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

SECRET_KEY = "jugal"  # Replace with your secret key
API_KEY_HEADER = "key_api"

class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request, call_next: RequestResponseEndpoint
    ):
        api_key = request.headers.get(API_KEY_HEADER)

        if api_key is None or api_key != SECRET_KEY:
            raise HTTPException(status_code=403, detail="Unauthorized")

        response = await call_next(request)
        return response